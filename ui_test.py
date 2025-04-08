from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os

def create_test_page():
    """Create a simple test page to demonstrate UI-API integration"""
    with open('test.html', 'w') as f:
        f.write("""
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
        """)

def test_ui_api_integration():
    """
    UI Test: Test interaction between UI and API via a simple web interface
    """
    # Create test page
    create_test_page()
    
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
