from locust import HttpUser, task, between

class ReconciliationUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def reconcile_get(self):
        self.client.get('/reconcile?query=Tolkien')

    @task
    def reconcile_post(self):
        payload = {
            'queries': {
                'q0': {'query': 'Orwell', 'limit': 3}
            }
        }
        self.client.post('/reconcile', json=payload)
