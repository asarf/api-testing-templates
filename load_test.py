from locust import HttpUser, task, between

class NationalizeLoadTest(HttpUser):
    wait_time = between(1, 2)  # Wait 1-2 seconds between tasks
    
    @task
    def test_name_prediction(self):
        """Load Test: Test API under normal load conditions"""
        names = ["john", "mary", "robert", "patricia", "michael"]
        for name in names:
            self.client.get(f"/?name={name}")
            
# Run with: locust -f load_test.py --host https://api.nationalize.io
