import requests
import random
import string
import urllib.parse

def generate_fuzz_name():
    """Generate various types of unexpected name inputs"""
    fuzz_types = [
        # Empty or whitespace
        "", " ", "   ",
        # Special characters
        "!@#$%^&*()", "\\n", "\\t", "<script>",
        # Very long names
        "a" * 1000,
        # Unicode characters
        "名字", "Señor", "Café",
        # Numbers and mixed
        "123", "name123", "123name",
        # SQL injection attempts
        "' OR '1'='1", "; DROP TABLE users;",
        # URL encoding tests
        urllib.parse.quote("name with spaces"),
        # Control characters
        "\x00", "\x1f", "\x7f"
    ]
    return random.choice(fuzz_types)

def test_api_fuzzing():
    """
    Fuzz Test: Send unexpected name formats to test API robustness
    """
    for _ in range(20):  # Run 20 fuzz tests
        fuzz_name = generate_fuzz_name()
        try:
            response = requests.get(f"https://api.nationalize.io/?name={fuzz_name}")
            
            # API should not crash
            assert response.status_code in range(200, 500)
            
            if response.status_code == 200:
                result = response.json()
                # Verify response structure even with fuzzy input
                assert "name" in result
                assert "country" in result
                assert isinstance(result["country"], list)
                
        except requests.exceptions.RequestException as e:
            # API should handle all inputs without crashing
            assert False, f"API crashed with: {str(e)}"
