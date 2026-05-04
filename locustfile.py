from locust import HttpUser, task, between

class APIUser(HttpUser):
    # Кожен "бот" буде чекати від 1 до 3 секунд між запитами
    wait_time = between(1, 3)

    @task
    def test_get_posts(self):
        # Тестуємо ендпоінт отримання всіх постів
        self.client.get("/posts")

    @task
    def test_get_single_post(self):
        # Тестуємо отримання конкретного поста (наприклад, ID=1)
        self.client.get("/posts/1")