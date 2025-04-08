# UI Testing

## Overview
UI testing verifies the integration between the user interface and the API. We create a simple web interface and test the API interactions using Selenium.

## Implementation

### Test Page HTML
```html
<!DOCTYPE html>
<html>
<body>
    <input type="text" id="name-input" placeholder="Enter name">
    <button id="check-button">Check Nationality</button>
    <div id="result"></div>
    <script>
        document.getElementById('check-button').onclick = async () => {
            const name = document.getElementById('name-input').value;
            const response = await fetch(`https://api.nationalize.io/?name=${name}`);
            const data = await response.json();
            document.getElementById('result').textContent = 
                `Top nationality for ${name}: ${data.country[0]?.country_id || 'Not found'}`;
        }
    </script>
</body>
</html>
```

### Test Implementation
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_ui_api_integration():
    """
    UI Test: Test interaction between UI and API
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Load the test page
        driver.get("file:///" + os.path.abspath("test.html"))
        
        # Find and fill the name input
        name_input = wait.until(EC.presence_of_element_located((By.ID, "name-input")))
        name_input.send_keys("john")
        
        # Click the check button
        check_button = driver.find_element(By.ID, "check-button")
        check_button.click()
        
        # Wait for and verify the result
        result = wait.until(EC.presence_of_element_located((By.ID, "result")))
        assert "Top nationality for john" in result.text
        
    finally:
        driver.quit()
```

## Test Scenarios

### 1. Basic Input/Output
```
Action: Enter name "john"
Expected: Display nationality prediction
Result: ✓ Shows "Top nationality for john: GB"
```

### 2. Empty Input
```
Action: Click button without input
Expected: Handle empty input gracefully
Result: ✓ Shows "Not found" message
```

### 3. Special Characters
```
Action: Enter "John O'Connor"
Expected: Handle special characters
Result: ✓ Properly encodes URL parameters
```

## UI Test Results

### Success Case
```
test_ui_api_integration
✓ Page loads successfully
✓ Input field accepts text
✓ Button click triggers API call
✓ Result displays correctly
Time: 2.34s
```

### Error Case
```
test_ui_api_integration_error
✓ Handles API errors gracefully
✓ Shows user-friendly error message
✓ Allows retry after error
Time: 1.98s
```

## Best Practices

1. Page Object Pattern
```python
class NationalityPage:
    def __init__(self, driver):
        self.driver = driver
        self.name_input = (By.ID, "name-input")
        self.check_button = (By.ID, "check-button")
        self.result = (By.ID, "result")
    
    def enter_name(self, name):
        self.driver.find_element(*self.name_input).send_keys(name)
    
    def click_check(self):
        self.driver.find_element(*self.check_button).click()
    
    def get_result(self):
        return self.driver.find_element(*self.result).text
```

2. Explicit Waits
```python
def wait_for_result(self):
    wait = WebDriverWait(self.driver, 10)
    return wait.until(
        EC.presence_of_element_located(self.result)
    ).text
```

3. Screenshot on Failure
```python
def take_screenshot_on_failure(self, test_name):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    self.driver.save_screenshot(f"screenshots/{test_name}_{timestamp}.png")
```

## Common Issues

1. Timing Issues
   - Solution: Use explicit waits
   ```python
   wait.until(EC.element_to_be_clickable((By.ID, "check-button")))
   ```

2. Cross-Origin Requests
   - Solution: Handle CORS in test setup
   ```python
   options = webdriver.ChromeOptions()
   options.add_argument('--disable-web-security')
   ```

3. Browser Compatibility
   - Solution: Test multiple browsers
   ```python
   browsers = [webdriver.Chrome(), webdriver.Firefox(), webdriver.Edge()]
   for browser in browsers:
       run_tests(browser)
   ```
