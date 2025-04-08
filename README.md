# API Testing Suite

A comprehensive API testing suite demonstrating 9 different types of API testing using the Nationalize.io API as an example.

## Test Types

1. **Smoke Test** (`smoke_test.py`)
   - Basic API health check
   - Verifies API accessibility and response structure

2. **Functional Test** (`functional_test.py`)
   - Tests core functionality
   - Validates nationality predictions for different names
   - Verifies response structure and data types

3. **Integration Test** (`integration_test.py`)
   - Tests name variations and case sensitivity
   - Validates consistency across multiple API calls
   - Checks probability calculations

4. **Regression Test** (`regression_test.py`)
   - Compares consecutive API calls
   - Ensures consistent behavior
   - Validates response stability

5. **Load Test** (`load_test.py`)
   - Uses Locust for load testing
   - Simulates normal usage patterns
   - Tests API performance under expected load

6. **Stress Test** (`stress_test.py`)
   - Aggressive load testing with Locust
   - Tests API behavior under heavy load
   - Uses random name generation

7. **Security Test** (`security_test.py`)
   - Tests SQL injection prevention
   - Validates rate limiting
   - Checks input sanitization

8. **UI Test** (`ui_test.py`)
   - Tests API integration with web interface
   - Uses Selenium WebDriver
   - Validates end-to-end functionality

9. **Fuzz Test** (`fuzz_test.py`)
   - Tests API robustness with unexpected inputs
   - Includes special characters, Unicode, and edge cases
   - Validates error handling

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

### Python Tests
Run all Python-based tests:
```bash
pytest smoke_test.py functional_test.py integration_test.py regression_test.py security_test.py ui_test.py fuzz_test.py -v
```

### Load Tests
Start the load test web interface:
```bash
locust -f load_test.py --host https://api.nationalize.io
```
Access the Locust dashboard at http://localhost:8089

### Stress Tests
Start the stress test web interface:
```bash
locust -f stress_test.py --host https://api.nationalize.io --web-port 8090
```
Access the Locust dashboard at http://localhost:8090

## Configuration

- The tests use the public Nationalize.io API
- No API key is required for basic usage
- Rate limiting may apply
- Adjust test parameters in respective files

## Requirements

- Python 3.8+
- pytest
- requests
- selenium
- locust
- Chrome WebDriver (for UI tests)

## Project Structure

```
api_testing/
├── README.md
├── requirements.txt
├── smoke_test.py
├── functional_test.py
├── integration_test.py
├── regression_test.py
├── load_test.py
├── stress_test.py
├── security_test.py
├── ui_test.py
└── fuzz_test.py
```

## Best Practices

1. **Test Independence**
   - Each test should run independently
   - No dependencies between test cases
   - Clean up after each test

2. **Error Handling**
   - All tests include proper error handling
   - Failed assertions provide clear messages
   - Exceptions are caught and reported

3. **Rate Limiting**
   - Respect API rate limits
   - Add delays between consecutive calls
   - Monitor response headers for limits

4. **Data Validation**
   - Verify response structures
   - Validate data types
   - Check edge cases

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add or modify tests
4. Submit a pull request

## License

MIT License - Feel free to use and modify for your own projects.
