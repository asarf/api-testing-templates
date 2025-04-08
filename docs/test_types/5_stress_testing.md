# Stress Testing

## Overview
Stress testing evaluates the API's behavior under extreme conditions. We use aggressive timing and random data to push the API to its limits.

## Implementation
```python
from locust import HttpUser, task, between
import random
import string

class NationalizeStressTest(HttpUser):
    wait_time = between(0.1, 0.5)  # Aggressive timing
    
    def generate_random_name(self, length):
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @task
    def stress_test_random_names(self):
        """Stress Test: Test API under heavy load with random names"""
        for length in [3, 5, 10, 20, 50]:
            random_name = self.generate_random_name(length)
            self.client.get(f"/?name={random_name}")
```

## Running Stress Tests
```bash
locust -f stress_test.py --host https://api.nationalize.io -u 100 -r 10
```

## Example Results

### Test Configuration
- Number of Users: 100
- Spawn Rate: 10 users/second
- Test Duration: 5 minutes

### Results Dashboard
```
Type     Name                      # reqs      # fails  |     Avg     Min     Max  
--------|--------------------------|------------|-------|-------|-------|-----------|
GET      /?name=[random]          15250   127(0.83%)  |   245    112    789  
--------|--------------------------|------------|-------|-------|-------|-----------|
         Aggregated               15250   127(0.83%)  |   245    112    789  
```

### Response Time Distribution
```
Percentage of requests completed within time (ms)
50%    245ms
66%    312ms
75%    356ms
80%    389ms
90%    478ms
95%    567ms
98%    678ms
99%    734ms
100%   789ms
```

## Performance Under Stress

### 1. Response Time Impact
```
Normal Load vs Stress Test
- Normal Avg: 88ms
- Stress Avg: 245ms
- Degradation: 178%
```

### 2. Error Rate Analysis
```
Error Types:
- Rate Limiting (429): 89 failures
- Timeout (504): 23 failures
- Server Error (500): 15 failures
```

### 3. Recovery Testing
```
Post-Stress Metrics (after 1 minute):
- Response Time: Returns to normal
- Error Rate: Drops to 0%
- Throughput: Stabilizes
```

## Key Observations

1. Breaking Points
   - Users: System shows strain at ~80 concurrent users
   - Requests/sec: Performance degrades at ~50 req/s
   - Response time: Exponential increase after 60 req/s

2. Error Patterns
   - Rate limiting kicks in at high concurrency
   - Timeout errors increase with load
   - Random server errors under extreme stress

3. Recovery Behavior
   - Quick recovery after load reduction
   - No permanent degradation observed
   - Rate limits reset as expected

## Best Practices

1. Gradual Stress Increase
   ```python
   class RampUpStressTest(HttpUser):
       def on_start(self):
           self.current_users = 0
           
       @task
       def increase_load(self):
           if self.current_users < 100:
               self.current_users += 10
   ```

2. Monitor System Health
   ```python
   @events.request.add_listener
   def on_request(request_type, name, response_time, response_length, **kwargs):
       if response_time > 500:
           log_warning(f"High latency detected: {response_time}ms")
   ```

3. Error Handling
   ```python
   try:
       response = self.client.get(f"/?name={name}")
       if response.status_code == 429:
           time.sleep(int(response.headers['Retry-After']))
   except Exception as e:
       log_error(f"Request failed: {str(e)}")
   ```

## Common Issues and Solutions

1. Rate Limiting
   - Issue: Too many requests (429)
   - Solution: Implement exponential backoff
   ```python
   def backoff_request(self, retries=3):
       for i in range(retries):
           try:
               return self.client.get(f"/?name={name}")
           except Exception:
               time.sleep(2 ** i)
   ```

2. Timeout Handling
   - Issue: Requests timing out
   - Solution: Adjust timeouts and implement retry logic
   ```python
   self.client.get(f"/?name={name}", 
                  timeout=5,
                  retry=True,
                  retry_delay=1)
