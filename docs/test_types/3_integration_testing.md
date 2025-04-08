# Integration Testing

## Overview
Integration testing verifies that different components of the API work together correctly. In this case, we test how the API handles different variations of the same name and ensures consistent results.

## Implementation
```python
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
```

## Test Scenarios
1. Case Sensitivity
   ```json
   // Request 1: /api/activity?name=john
   {
     "name": "john",
     "country": [
       {"country_id": "IE", "probability": 0.453},
       {"country_id": "GB", "probability": 0.321}
     ]
   }

   // Request 2: /api/activity?name=John
   {
     "name": "John",
     "country": [
       {"country_id": "IE", "probability": 0.453},
       {"country_id": "GB", "probability": 0.321}
     ]
   }
   ```

2. Probability Validation
   ```python
   total_probability = sum(country["probability"] for country in result["country"])
   assert total_probability <= 1.0  # Probabilities should not sum to more than 1
   ```

## Integration Points
1. Name Normalization
   - Case handling
   - Whitespace handling
   - Special character handling

2. Probability Calculations
   - Consistent across requests
   - Mathematically sound
   - Properly normalized

3. Response Consistency
   - Same structure
   - Consistent data types
   - Reliable ordering

## Common Integration Issues
1. Inconsistent Case Handling
   - Different results for same name with different cases
   - Inconsistent normalization

2. Probability Inconsistencies
   - Probabilities not properly normalized
   - Inconsistent rounding
   - Mathematical errors

3. Response Format Issues
   - Inconsistent field names
   - Different data types
   - Missing fields

## Best Practices
1. Test Multiple Variations
   - Different cases
   - Different formats
   - Different lengths

2. Validate Data Consistency
   - Compare responses
   - Check mathematical properties
   - Verify data types

3. Monitor Response Times
   - Track timing differences
   - Check for degradation
   - Verify SLA compliance
