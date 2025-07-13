import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time

# Automatically install the ChromeDriver
chromedriver_autoinstaller.install()

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Uncomment to run headless once confirmed working
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(), options=options)

try:
    print("🌐 Connecting to LeetCode login page...")
    driver.get("https://leetcode.com/accounts/login/")

    # Replace with your actual LeetCode username and password here
    username = "your_leetcode_username"
    password = "your_leetcode_password"

    wait = WebDriverWait(driver, 15)

    print("🔐 Waiting for login fields...")
    # LeetCode login inputs have name 'login' and 'password'
    user_input = wait.until(EC.presence_of_element_located((By.NAME, "login")))
    pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    print("✍️ Entering credentials...")
    user_input.clear()
    user_input.send_keys(username)
    pass_input.clear()
    pass_input.send_keys(password)

    print("🚀 Clicking Sign in button...")
    sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]")))
    sign_in_button.click()

    # Wait a bit for login to process and page to load
    time.sleep(5)

    # Confirm login by checking presence of profile icon or redirect
    print("✅ Logged in. Navigating to submissions page...")
    driver.get("https://leetcode.com/submissions/")

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/submissions/detail/')]")))

    print("📌 Opening latest submission...")
    latest = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    latest.click()

    # Wait for the code editor content to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ace_content")))

    # Extract code text
    code = driver.find_element(By.CLASS_NAME, "ace_content").text.strip()
    title = driver.title.split(" - ")[0].strip()
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Save solution to file
    solution_dir = os.path.join(os.path.dirname(__file__), "../leetcode-solutions")
    os.makedirs(solution_dir, exist_ok=True)
    filename = f"{date_str}_{title.replace(' ', '_').replace('/', '_')}.txt"
    file_path = os.path.join(solution_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"✅ Code saved to: {file_path}")

except Exception as e:
    print("❌ Error occurred:", e)

finally:
    driver.quit()
