import os
import json
import pytest
from unittest.mock import patch, MagicMock
from backend.updater import KnowledgeBaseUpdater, FileInfo

@pytest.fixture
def updater():
    return KnowledgeBaseUpdater(
        github_token="test_token",
        repo_owner="test_owner",
        repo_name="test_repo",
        embeddings_file="tests/test_embeddings.json",
        gemini_api_key="test_api_key"
    )

def test_load_existing_embeddings(updater):
    # Create a dummy embeddings file
    dummy_data = [{"file_path": "test.md", "embedding": [0.1, 0.2, 0.3]}]
    with open(updater.embeddings_file, "w") as f:
        json.dump(dummy_data, f)

    embeddings = updater._load_existing_embeddings()
    assert len(embeddings) == 1
    assert embeddings[0]["file_path"] == "test.md"

    os.remove(updater.embeddings_file)

@patch("backend.updater.KnowledgeBaseUpdater._get_github_files_async")
@patch("backend.updater.KnowledgeBaseUpdater._process_files_batch")
async def test_update_knowledge_base(mock_process_files_batch, mock_get_github_files, updater):
    mock_get_github_files.return_value = [FileInfo(path="test.md", sha="123")]
    mock_process_files_batch.return_value = [
        {
            "file_path": "test.md",
            "content": "Test content",
            "embedding": [0.1, 0.2, 0.3],
            "file_hash": "abc",
            "file_size": 12,
            "updated_at": "2025-09-09T12:00:00"
        }
    ]

    result = await updater.update_knowledge_base()
    assert result["files_processed"] == 1
    assert result["total_files"] == 1

    assert os.path.exists(updater.embeddings_file)
    os.remove(updater.embeddings_file)
