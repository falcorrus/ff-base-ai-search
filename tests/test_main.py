import os
from fastapi.testclient import TestClient
from main import app, load_knowledge_base

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_search_empty_query():
    response = client.get("/search?query=")
    assert response.status_code == 400
    assert response.json() == {"detail": "Query cannot be empty."}

def test_search_no_knowledge_base():
    # Make sure the knowledge base is empty
    load_knowledge_base()
    if os.path.exists("knowledge_base/embeddings.json"):
        os.remove("knowledge_base/embeddings.json")
    load_knowledge_base()

    response = client.get("/search?query=test")
    assert response.status_code == 200
    assert response.json()["answer"] == 'There is no context provided.  Therefore, I cannot answer the query "test".\n'
