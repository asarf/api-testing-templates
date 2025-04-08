import requests
import pytest
import time

def test_api_regression():
    """
    Regression Test: Compare responses between consecutive API calls
    """
    test_name = "michael"
    
    # First API call
    first_response = requests.get(f"https://api.nationalize.io/?name={test_name}")
    first_result = first_response.json()
    
    # Wait briefly
    time.sleep(1)
    
    # Second API call
    second_response = requests.get(f"https://api.nationalize.io/?name={test_name}")
    second_result = second_response.json()
    
    # Compare results - they should be consistent
    assert first_result["name"] == second_result["name"]
    assert len(first_result["country"]) == len(second_result["country"])
    
    # Compare top country predictions
    if first_result["country"] and second_result["country"]:
        assert first_result["country"][0]["country_id"] == second_result["country"][0]["country_id"]
