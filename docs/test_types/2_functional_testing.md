# Functional Testing

## Overview
Functional testing ensures that the API behaves according to its specifications. It validates that the API correctly processes input and returns expected results.

## Implementation
```python
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
        
        if result["country"]:
            country = result["country"][0]
            assert "country_id" in country
            assert "probability" in country
            assert isinstance(country["probability"], float)
            assert 0 <= country["probability"] <= 1
```

## Example Results
```json
{
    "name": "james",
    "country": [
        {
            "country_id": "GB",
            "probability": 0.481
        },
        {
            "country_id": "US",
            "probability": 0.321
        }
    ]
}
```

## Test Cases
1. Common Names
   - Western names (e.g., "james")
   - Hispanic names (e.g., "maria")
   - Arabic names (e.g., "mohammed")
   - Asian names (e.g., "yuki")
   - European names (e.g., "hans")

2. Data Validation
   - Name field matches input
   - Country list is present
   - Probabilities are valid floats
   - Country codes are valid

3. Response Structure
   - JSON format
   - Required fields present
   - Correct data types

## Success Criteria
- Status code 200
- Valid JSON response
- Correct response structure
- Probability values between 0 and 1
- Valid country codes

## Common Issues
1. Invalid name formats
2. Missing response fields
3. Incorrect probability calculations
4. Invalid country codes
