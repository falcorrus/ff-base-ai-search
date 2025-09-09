#!/usr/bin/env python3
import os
import sys
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from updater_enhanced import KnowledgeBaseUpdater

# Add the python directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables
load_dotenv()

# Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Gemini
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

genai.configure(api_key=GEMINI_API_KEY)

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_PAT")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_PAT environment variable is not set.")

GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER", "falcorrus")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "ff-base")

# Data
EMBEDDINGS_FILE = "knowledge_base/embeddings.json"

async def test_enhanced_updater():
    """Test the enhanced updater with pagination support"""
    print("Testing enhanced updater with pagination support...")
    
    updater = KnowledgeBaseUpdater(
        github_token=GITHUB_TOKEN,
        repo_owner=GITHUB_REPO_OWNER,
        repo_name=GITHUB_REPO_NAME,
        embeddings_file=EMBEDDINGS_FILE,
        gemini_api_key=GEMINI_API_KEY,
    )
    
    try:
        result = await updater.update_knowledge_base()
        print(f"Update result: {result}")
        return result
    except Exception as e:
        print(f"Error during update: {e}")
        return None

if __name__ == "__main__":
    result = asyncio.run(test_enhanced_updater())
    if result:
        print("Enhanced updater test completed successfully!")
        print(f"Files processed: {result.get('files_processed', 0)}")
        print(f"Files skipped: {result.get('files_skipped', 0)}")
        print(f"Total files in knowledge base: {result.get('total_files', 0)}")
    else:
        print("Enhanced updater test failed!")
        sys.exit(1)