from locust import HttpUser, task, between
import random
import string

class NationalizeStressTest(HttpUser):
    wait_time = between(0.1, 0.5)  # Aggressive timing for stress test
    
    def generate_random_name(self, length):
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @task
    def stress_test_random_names(self):
        """Stress Test: Test API under heavy load with random names"""
        # Generate random name lengths to stress test
        for length in [3, 5, 10, 20, 50]:
            random_name = self.generate_random_name(length)
            self.client.get(f"/?name={random_name}")

# Run with: locust -f stress_test.py --host https://api.nationalize.io -u 100 -r 10
