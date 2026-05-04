import pytest
from fastapi.testclient import TestClient
from main import app  # Імпортуємо твій об'єкт FastAPI

client = TestClient(app)


# 1. Простий тест на доступність головної сторінки або постів
def test_read_posts():
    response = client.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 2. СКЛАДНИЙ СЦЕНАРІЙ (Complex Scenario)
# Створюємо пост -> отримуємо його ID -> використовуємо ID для перевірки
def test_post_creation_and_retrieval_flow():
    # Крок А: Створюємо новий пост
    new_post_data = {
        "title": "Test Lab 4",
        "content": "Testing coverage and logic",
        "authorId": 1
    }
    create_res = client.post("/posts", json=new_post_data)

    # Перевіряємо, чи пост створився (код 201)
    assert create_res.status_code == 201
    created_post = create_res.json()
    post_id = created_post["id"]  # Отримуємо ID створеного поста

    # Крок Б: Використовуємо цей ID, щоб отримати саме цей пост
    get_res = client.get(f"/posts/{post_id}")

    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Test Lab 4"
    assert get_res.json()["id"] == post_id