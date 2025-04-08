import requests
import pytest

def test_api_health():
    """
    Smoke Test: Simple health check to verify Nationalize API is responding
    """
    response = requests.get("https://api.nationalize.io/?name=john")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "country" in response.json()
