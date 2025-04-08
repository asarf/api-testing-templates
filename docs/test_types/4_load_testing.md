# Load Testing

## Overview
Load testing evaluates the API's performance under expected load conditions. We use Locust to simulate multiple users accessing the API simultaneously.

## Implementation
```python
from locust import HttpUser, task, between

class NationalizeLoadTest(HttpUser):
    wait_time = between(1, 2)  # Wait 1-2 seconds between tasks
    
    @task
    def test_name_prediction(self):
        """Load Test: Test API under normal load conditions"""
        names = ["john", "mary", "robert", "patricia", "michael"]
        for name in names:
            self.client.get(f"/?name={name}")
```

## Running Load Tests
```bash
locust -f load_test.py --host https://api.nationalize.io
```

## Example Results

### Test Configuration
- Number of Users: 10
- Spawn Rate: 1 user/second
- Test Duration: 5 minutes

### Results Dashboard
```
Type     Name                      # reqs      # fails  |     Avg     Min     Max  
--------|--------------------------|------------|-------|-------|-------|-----------|
GET      /?name=john               1250    0(0.00%)  |    89    65    213  
GET      /?name=mary               1248    0(0.00%)  |    87    63    198  
GET      /?name=robert             1247    0(0.00%)  |    88    64    201  
--------|--------------------------|------------|-------|-------|-------|-----------|
         Aggregated                3745    0(0.00%)  |    88    63    213  
```

### Response Time Distribution
```
Percentage of requests completed within time (ms)
50%    88ms
66%    95ms
75%    99ms
80%    102ms
90%    112ms
95%    123ms
98%    145ms
99%    167ms
100%   213ms
```

## Key Metrics
1. Response Times
   - Average: 88ms
   - Median (50%): 88ms
   - 95th percentile: 123ms
   - Maximum: 213ms

2. Throughput
   - Requests per second: ~12.5
   - Total requests: 3,745
   - Failed requests: 0

3. Error Rates
   - Success rate: 100%
   - Error rate: 0%

## Performance Thresholds
1. Response Times
   - Target average: < 100ms
   - Target 95th percentile: < 200ms
   - Maximum acceptable: < 500ms

2. Error Rates
   - Target: < 0.1%
   - Maximum acceptable: < 1%

3. Throughput
   - Minimum: 10 req/s
   - Target: 20 req/s
   - Maximum tested: 50 req/s

## Common Issues
1. Response Time Degradation
   - Causes: High concurrency, database bottlenecks
   - Solution: Optimize queries, add caching

2. Error Rate Spikes
   - Causes: Rate limiting, resource exhaustion
   - Solution: Implement backoff, increase capacity

3. Throughput Limitations
   - Causes: API limitations, network constraints
   - Solution: Distribution, load balancing

## Best Practices
1. Gradual Load Increase
   - Start with low user count
   - Increase gradually
   - Monitor for degradation

2. Realistic Scenarios
   - Use real-world patterns
   - Vary request types
   - Include think time

3. Continuous Monitoring
   - Watch all metrics
   - Set up alerts
   - Log issues
