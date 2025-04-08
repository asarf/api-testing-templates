import requests
import pytest

def test_name_variations():
    """
    Integration Test: Test nationality predictions for name variations
    """
    # Step 1: Test original name
    base_name = "john"
    base_response = requests.get(f"https://api.nationalize.io/?name={base_name}")
    assert base_response.status_code == 200
    base_result = base_response.json()
    
    # Step 2: Test capitalized version
    cap_name = base_name.capitalize()
    cap_response = requests.get(f"https://api.nationalize.io/?name={cap_name}")
    assert cap_response.status_code == 200
    cap_result = cap_response.json()
    
    # Step 3: Compare results (should be case-insensitive)
    assert len(base_result["country"]) == len(cap_result["country"])
    
    # Step 4: Verify probabilities sum is less than or equal to 1
    total_probability = sum(country["probability"] for country in base_result["country"])
    assert total_probability <= 1.0
