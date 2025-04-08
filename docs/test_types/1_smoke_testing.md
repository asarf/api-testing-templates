# Smoke Testing

## Overview
Smoke testing verifies that the most critical functions of the API work correctly. It's the first line of defense against major failures.

## Implementation
```python
def test_api_health():
    """
    Smoke Test: Simple health check to verify Nationalize API is responding
    """
    response = requests.get("https://api.nationalize.io/?name=john")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "country" in response.json()
```

## Example Results
```
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-7.4.3
collecting ... collected 1 item

smoke_test.py::test_api_health PASSED                                    [100%]

============================== 1 passed in 1.52s =============================
```

## Key Points
- Fast execution (< 2 seconds)
- Checks basic API availability
- Validates response structure
- No detailed data validation

## When to Use
- After deployment
- Before running detailed tests
- During continuous integration
- For quick health checks

## Common Issues
1. Network connectivity problems
2. API endpoint changes
3. Basic authentication issues
4. Response format changes
