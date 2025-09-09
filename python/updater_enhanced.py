import os
import json
import asyncio
import aiohttp
import hashlib
import base64
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from fastapi import HTTPException
import google.generativeai as genai

@dataclass
class FileInfo:
    path: str
    sha: str
    size: int = 0

class KnowledgeBaseUpdater:
    def __init__(self, github_token: str, repo_owner: str, repo_name: str, 
                 embeddings_file: str, gemini_api_key: str, batch_size: int = 3, 
                 max_file_size: int = 1024 * 1024, rate_limit_delay: float = 0.1,
                 max_recursion_depth: int = 10):
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.embeddings_file = embeddings_file
        self.max_file_size = max_file_size
        self.max_recursion_depth = max_recursion_depth
        self.rate_limit_delay = rate_limit_delay
        self.batch_size = batch_size
        
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.embedding_model = "models/embedding-001"
        else:
            raise ValueError("GEMINI_API_KEY is required")
        
    async def update_knowledge_base(self) -> Dict:
        """Улучшенная версия обновления базы знаний с поддержкой всех файлов"""
        try:
            print("Starting knowledge base update...")
            
            # Используем новый метод для получения всех файлов
            files = await self._get_all_github_files_with_pagination()
            if not files:
                return {"message": "No files found or error occurred", "files_processed": 0}
            
            print(f"Found {len(files)} files to process")
            
            existing_embeddings = self._load_existing_embeddings()
            existing_hashes = {
                item.get("file_hash"): item 
                for item in existing_embeddings 
                if item.get("file_hash")
            }
            
            print(f"Loaded {len(existing_hashes)} existing embeddings")
            
            embeddings_data = []
            processed_count = 0
            skipped_count = 0
            
            for i in range(0, len(files), self.batch_size):
                batch = files[i:i + self.batch_size]
                print(f"Processing batch {i//self.batch_size + 1}/{(len(files) + self.batch_size - 1)//self.batch_size}")
                
                batch_results = await self._process_files_batch(batch, existing_hashes)
                
                for result in batch_results:
                    if result:
                        if result.get("skipped"):
                            skipped_count += 1
                        else:
                            embeddings_data.append(result)
                            processed_count += 1
            
            all_embeddings = embeddings_data + [
                item for item in existing_hashes.values() 
                if item.get("file_hash") not in [e.get("file_hash") for e in embeddings_data]
            ]
            
            await self._save_embeddings_with_backup(all_embeddings)
            
            return {
                "message": f"Knowledge base updated successfully",
                "files_processed": processed_count,
                "files_skipped": skipped_count,
                "total_files": len(all_embeddings)
            }
            
        except Exception as e:
            print(f"Error in update_knowledge_base: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Failed to update knowledge base: {str(e)}")
    
    async def _get_all_github_files_with_pagination(self) -> List[FileInfo]:
        """Получение всех .md файлов из репозитория с использованием Contents API и пагинации"""
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        all_files = []
        page = 1
        per_page = 100  # Максимальное количество элементов на странице
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
        ) as session:
            while True:
                # Используем поиск для нахождения всех .md файлов
                search_url = (f"https://api.github.com/search/code?"
                             f"q=repo:{self.repo_owner}/{self.repo_name}+extension:.md&"
                             f"per_page={per_page}&page={page}")
                
                try:
                    await asyncio.sleep(self.rate_limit_delay)
                    async with session.get(search_url) as response:
                        if response.status == 200:
                            data = await response.json()
                            items = data.get("items", [])
                            
                            if not items:
                                break
                            
                            # Добавляем найденные файлы
                            for item in items:
                                file_info = FileInfo(
                                    path=item["path"],
                                    sha=item["sha"],
                                    size=0  # Размер будет получен позже при необходимости
                                )
                                all_files.append(file_info)
                            
                            # Проверяем, есть ли еще страницы
                            if len(items) < per_page:
                                break
                            
                            page += 1
                            
                            # Ограничиваем количество запросов для бесплатного тарифа GitHub
                            if page > 30:  # Ограничение для бесплатного тарифа (3000 запросов/час)
                                print("Reached GitHub API rate limit, stopping pagination")
                                break
                        else:
                            print(f"Error searching files: {response.status}")
                            break
                except Exception as e:
                    print(f"Exception in file search: {e}")
                    break
            
            print(f"Total .md files found via search: {len(all_files)}")
            return all_files
    
    async def _get_github_files_async(self) -> List[FileInfo]:
        """Оригинальный метод для обратной совместимости"""
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers=headers
        ) as session:
            try:
                commit_sha = await self._get_main_branch_sha(session)
                if not commit_sha:
                    return []
                
                tree_sha = await self._get_tree_sha(session, commit_sha)
                if not tree_sha:
                    return []
                
                all_files = []
                await self._fetch_tree_recursive_async(session, tree_sha, "", all_files, 0)
                
                print(f"Total .md files found: {len(all_files)}")
                return all_files
                
            except Exception as e:
                print(f"Error fetching GitHub files: {e}")
                return []
    
    async def _get_main_branch_sha(self, session: aiohttp.ClientSession) -> Optional[str]:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/git/ref/heads/main"
        
        try:
            await asyncio.sleep(self.rate_limit_delay)
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    sha = data["object"]["sha"]
                    print(f"Main branch SHA: {sha}")
                    return sha
                else:
                    print(f"Error fetching main branch ref: {response.status}")
                    response_text = await response.text()
                    print(f"Response: {response_text}")
                    return None
        except Exception as e:
            print(f"Exception getting main branch SHA: {e}")
            return None
    
    async def _get_tree_sha(self, session: aiohttp.ClientSession, commit_sha: str) -> Optional[str]:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/git/commits/{commit_sha}"
        
        try:
            await asyncio.sleep(self.rate_limit_delay)
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    tree_sha = data["tree"]["sha"]
                    print(f"Tree SHA: {tree_sha}")
                    return tree_sha
                else:
                    print(f"Error fetching commit details: {response.status}")
                    return None
        except Exception as e:
            print(f"Exception getting tree SHA: {e}")
            return None

    async def _fetch_tree_recursive_async(
        self, 
        session: aiohttp.ClientSession, 
        tree_sha: str, 
        current_path: str,
        all_files: List[FileInfo],
        depth: int
    ) -> None:
        if depth >= self.max_recursion_depth:
            print(f"Maximum recursion depth reached at path: {current_path}")
            return
        
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/git/trees/{tree_sha}"
        
        try:
            await asyncio.sleep(self.rate_limit_delay)
            
            async with session.get(url) as response:
                if response.status == 200:
                    tree_data = await response.json()
                    
                    subtree_tasks = []
                    
                    for item in tree_data.get("tree", []):
                        full_path = f"{current_path}/{item['path']}" if current_path else item["path"]
                        
                        if item["type"] == "blob" and full_path.endswith(".md"):
                            if item.get("size", 0) <= self.max_file_size:
                                all_files.append(FileInfo(
                                    path=full_path,
                                    sha=item["sha"],
                                    size=item.get("size", 0)
                                ))
                            else:
                                print(f"Skipping large file: {full_path} ({item.get('size', 0)} bytes)")
                                
                        elif item["type"] == "tree":
                            task = self._fetch_tree_recursive_async(
                                session, item["sha"], full_path, all_files, depth + 1
                            )
                            subtree_tasks.append(task)
                    
                    if subtree_tasks:
                        semaphore = asyncio.Semaphore(3)
                        
                        async def bounded_task(task):
                            async with semaphore:
                                return await task
                        
                        bounded_tasks = [bounded_task(task) for task in subtree_tasks]
                        await asyncio.gather(*bounded_tasks, return_exceptions=True)
                        
                else:
                    print(f"Error fetching tree {tree_sha}: {response.status}")
                    
        except Exception as e:
            print(f"Exception in fetch_tree_recursive_async: {e}")
    
    async def _process_files_batch(
        self, 
        files: List[FileInfo], 
        existing_hashes: Dict[str, Dict]
    ) -> List[Optional[Dict]]:
        tasks = []
        for file_info in files:
            task = self._process_single_file(file_info, existing_hashes)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error processing file {files[i].path}: {result}")
            elif result:
                valid_results.append(result)
        
        return valid_results
    
    async def _process_single_file(
        self, 
        file_info: FileInfo, 
        existing_hashes: Dict[str, Dict]
    ) -> Optional[Dict]:
        try:
            print(f"Processing file: {file_info.path}")
            
            content = await self._get_file_content_async(file_info.sha)
            if not content:
                print(f"Failed to get content for: {file_info.path}")
                return None
            
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            
            if content_hash in existing_hashes:
                print(f"File unchanged, skipping: {file_info.path}")
                return {"skipped": True}
            
            if not self._validate_content(content):
                print(f"Content validation failed for: {file_info.path}")
                return None
            
            print(f"Generating embedding for: {file_info.path}")
            embedding = await self._generate_embedding_async(content)
            if embedding is None:
                print(f"Failed to generate embedding for: {file_info.path}")
                return None
            
            print(f"Successfully processed: {file_info.path}")
            return {
                "file_path": file_info.path,
                "content": content,
                "embedding": embedding,
                "file_hash": content_hash,
                "file_size": file_info.size,
                "updated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error processing file {file_info.path}: {e}")
            return None
    
    async def _get_file_content_async(self, file_sha: str) -> Optional[str]:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/git/blobs/{file_sha}"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                await asyncio.sleep(self.rate_limit_delay)
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data["content"]
                        decoded_content = base64.b64decode(content).decode("utf-8")
                        return decoded_content
                    else:
                        print(f"Error fetching file content for {file_sha}: {response.status}")
                        return None
        except Exception as e:
            print(f"Exception getting file content for {file_sha}: {e}")
            return None
    
    async def _generate_embedding_async(self, text: str) -> Optional[List[float]]:
        try:
            loop = asyncio.get_event_loop()
            
            def generate_sync():
                return genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document"
                )
            
            result = await loop.run_in_executor(None, generate_sync)
            return result["embedding"]
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def _validate_content(self, content: str) -> bool:
        if not content or len(content.strip()) == 0:
            return False
        
        try:
            content.encode('utf-8')
        except UnicodeEncodeError:
            return False
        
        if len(content) > self.max_file_size:
            return False
        
        if len(content.strip()) < 10:
            return False
        
        return True
    
    def _load_existing_embeddings(self) -> List[Dict]:
        if os.path.exists(self.embeddings_file):
            try:
                with open(self.embeddings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"Loaded {len(data)} existing embeddings")
                    return data
            except Exception as e:
                print(f"Error loading embeddings: {e}")
                return []
        print("No existing embeddings file found")
        return []
    
    async def _save_embeddings_with_backup(self, embeddings_data: List[Dict]) -> None:
        os.makedirs(os.path.dirname(self.embeddings_file), exist_ok=True)
        
        if os.path.exists(self.embeddings_file):
            backup_path = f"{self.embeddings_file}.backup"
            shutil.copy2(self.embeddings_file, backup_path)
            print(f"Backup created: {backup_path}")
        
        try:
            with open(self.embeddings_file, "w", encoding="utf-8") as f:
                json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
            print(f"Successfully saved {len(embeddings_data)} embeddings")
            
        except Exception as e:
            print(f"Error saving embeddings: {e}")
            backup_path = f"{self.embeddings_file}.backup"
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.embeddings_file)
                print("Restored from backup due to save error")
            raise e