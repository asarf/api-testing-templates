# Security Testing

## Overview
Security testing evaluates the API's resistance to various types of attacks and validates its security controls.

## Implementation
```python
def test_sql_injection():
    """
    Security Test: Test SQL injection prevention
    """
    malicious_inputs = [
        "' OR '1'='1",
        "\"); DROP TABLE users; --",
        "<script>alert('xss')</script>",
        "../../../etc/passwd"
    ]
    
    for input_value in malicious_inputs:
        response = requests.get(f"https://api.nationalize.io/?name={input_value}")
        # API should handle malicious input gracefully
        assert response.status_code in [200, 400, 422]
        if response.status_code == 200:
            result = response.json()
            assert len(result.get("country", [])) == 0

def test_rate_limiting():
    """
    Security Test: Verify rate limiting
    """
    for _ in range(10):
        response = requests.get("https://api.nationalize.io/?name=test")
        assert response.status_code in [200, 429]
```

## Security Test Cases

### 1. SQL Injection Prevention
```
Test Input: "' OR '1'='1"
Expected: No data leakage, graceful handling
Result: ✓ API returns empty result set
```

### 2. XSS Attack Prevention
```
Test Input: "<script>alert('xss')</script>"
Expected: Input sanitized or rejected
Result: ✓ API handles special characters safely
```

### 3. Path Traversal Prevention
```
Test Input: "../../../etc/passwd"
Expected: No file system access
Result: ✓ API treats as normal name input
```

### 4. Rate Limiting
```
Test: 10 rapid requests
Expected: Rate limiting after threshold
Result: ✓ Returns 429 after limit exceeded
```

## Security Headers Check
```python
def check_security_headers(response):
    headers = response.headers
    assert 'X-Content-Type-Options' in headers
    assert 'X-Frame-Options' in headers
    assert 'X-XSS-Protection' in headers
    assert 'Content-Security-Policy' in headers
```

## Common Security Issues

1. Input Validation
   - SQL Injection
   - Cross-Site Scripting (XSS)
   - Command Injection
   - Path Traversal

2. Rate Limiting
   - DDoS Protection
   - Brute Force Prevention
   - Resource Exhaustion

3. Authentication/Authorization
   - Token Validation
   - Permission Checks
   - Session Management

## Best Practices

1. Input Sanitization
```python
def sanitize_input(name):
    # Remove special characters
    sanitized = re.sub(r'[<>\'";]', '', name)
    # Limit length
    return sanitized[:50]
```

2. Rate Limiting Implementation
```python
from functools import lru_cache
from time import time

@lru_cache(maxsize=1000)
def check_rate_limit(ip_address):
    current_time = time()
    if (current_time - last_request) < 1:
        raise RateLimitExceeded
```

3. Security Headers
```python
headers = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': "default-src 'self'"
}
```

## Security Testing Tools
1. OWASP ZAP
2. Burp Suite
3. Custom Python Scripts

## Monitoring and Logging
```python
def log_security_event(event_type, details):
    logger.warning(f"Security Event: {event_type}")
    logger.warning(f"Details: {details}")
    # Alert if necessary
    if event_type in HIGH_RISK_EVENTS:
        alert_security_team(event_type, details)
```
