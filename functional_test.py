import requests
import pytest

def test_name_nationality_prediction():
    """
    Functional Test: Verify name nationality prediction functionality
    """
    test_names = ["james", "maria", "mohammed", "yuki", "hans"]
    
    for name in test_names:
        response = requests.get(f"https://api.nationalize.io/?name={name}")
        assert response.status_code == 200
        
        result = response.json()
        assert result["name"] == name
        assert isinstance(result["country"], list)
        
        # Check country prediction structure
        if result["country"]:
            country = result["country"][0]
            assert "country_id" in country
            assert "probability" in country
            assert isinstance(country["probability"], float)
            assert 0 <= country["probability"] <= 1
