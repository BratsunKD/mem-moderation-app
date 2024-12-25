import time
import math
import random
from locust import HttpUser, task, between


texts = ["text1", "text22", "text333", "text4444", "text55555"]


class QuickstartUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def text_moderation(self):
        message = {
            "text": random.choice(texts),
            "user_id": random.randint(1, 50),
            "text_id": random.randint(1, 35),
        }
        self.client.post('/text-moderation/', json=message)

    @task
    def get_prediction(self):
        message = {
            "text": random.choice(texts),
            "user_id": random.randint(1, 50),
            "text_id": random.randint(1, 35),
        }
        self.client.post('/get-result/', json=message)
