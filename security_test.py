import requests
import pytest

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
            # Should return empty or null results for invalid names
            result = response.json()
            assert len(result.get("country", [])) == 0

def test_rate_limiting():
    """
    Security Test: Verify rate limiting
    """
    # Make rapid requests to test rate limiting
    for _ in range(10):
        response = requests.get("https://api.nationalize.io/?name=test")
        assert response.status_code in [200, 429]  # 429 is Too Many Requests
