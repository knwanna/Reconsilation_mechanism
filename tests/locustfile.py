from locust import HttpUser, task, constant
import random

class ReconciliationUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = constant(1)

    @task
    def reconcile_get_query(self):
        queries = ["George Orwell", "Lord of", "Gatsbyy", "J.R.R. Tolkin", "Jane Austen", "NonExistentBook"]
        query = random.choice(queries)
        response = self.client.get(f"/reconcile?query={query}")
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    @task
    def reconcile_post_query(self):
        queries = ["George Orwell", "Lord of", "Gatsbyy", "J.R.R. Tolkin", "Jane Austen"]
        payload = {
            "queries": {
                "q0": {"query": random.choice(queries), "limit": 3},
                "q1": {"query": random.choice(queries), "limit": 3}
            }
        }
        response = self.client.post("/reconcile", json=payload)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
