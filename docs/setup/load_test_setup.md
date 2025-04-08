# Load Test Setup Guide

## Prerequisites
1. Python 3.8+ installed
2. pip package manager
3. Virtual environment tool
4. Git (optional)

## Step-by-Step Setup

### 1. Create Project Directory
```bash
mkdir api_testing
cd api_testing
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install locust requests pytest pytest-html
```

### 4. Create Load Test Script
Create `load_test.py`:
```python
from locust import HttpUser, task, between
import random

class NationalizeLoadTest(HttpUser):
    wait_time = between(1, 2)
    
    def on_start(self):
        """Initialize test data"""
        self.test_names = ["john", "mary", "robert", "patricia", "michael"]
        self.current_users = 0
    
    @task
    def test_name_prediction(self):
        """Test name nationality prediction under load"""
        name = random.choice(self.test_names)
        with self.client.get(
            f"/?name={name}", 
            catch_response=True
        ) as response:
            if response.status_code == 200:
                # Validate response structure
                data = response.json()
                if "name" in data and "country" in data:
                    response.success()
                else:
                    response.failure("Invalid response structure")
            elif response.status_code == 429:
                response.failure("Rate limited")
```

### 5. Configure Locust
Create `locust.conf`:
```ini
host = https://api.nationalize.io
users = 10
spawn-rate = 1
run-time = 5m
headless = false
web-port = 8089
```

### 6. Create HTML Report Template
Create `report_template.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Load Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .chart { margin: 20px; padding: 10px; }
        .metric { 
            border: 1px solid #ddd;
            padding: 10px;
            margin: 5px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <h1>Load Test Results</h1>
    <div id="metrics"></div>
    <div id="charts"></div>
</body>
</html>
```

## Running Tests

### 1. Basic Run
```bash
locust -f load_test.py
```

### 2. Headless Mode with Report
```bash
locust -f load_test.py --headless --users 10 --spawn-rate 1 --run-time 5m --html report.html
```

### 3. Custom Configuration
```bash
locust -f load_test.py --config locust.conf
```

## Monitoring Tests

### 1. Web Interface
- Open http://localhost:8089 in browser
- Enter number of users and spawn rate
- Click "Start swarming"

### 2. Real-time Metrics
- Request count
- Response times
- Error rates
- RPS (Requests Per Second)

### 3. Console Output
```bash
locust -f load_test.py --print-stats
```

## Advanced Configuration

### 1. Custom Load Shape
```python
from locust import LoadTestShape

class StagesShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 1},
        {"duration": 120, "users": 20, "spawn_rate": 2},
        {"duration": 180, "users": 30, "spawn_rate": 3},
    ]
    
    def tick(self):
        run_time = self.get_run_time()
        
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None
```

### 2. Custom Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='load_test.log'
)
```

### 3. Rate Limiting Handling
```python
from locust import events

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, **kwargs):
    if response.status_code == 429:
        # Wait before next request
        time.sleep(int(response.headers.get('Retry-After', 5)))
```

## Troubleshooting

### 1. Common Issues
- Port already in use
  ```bash
  locust -f load_test.py --web-port 8090
  ```

- Memory issues
  ```bash
  # Limit memory usage
  export LOCUST_MAX_MEMORY=1024
  ```

- Connection errors
  ```python
  # Add retry logic
  self.client.get(url, retry_count=3, retry_delay=1)
  ```

### 2. Performance Tips
- Use connection pooling
- Implement proper wait times
- Monitor system resources
- Use appropriate user counts

### 3. Debug Mode
```bash
locust -f load_test.py --loglevel DEBUG
```
