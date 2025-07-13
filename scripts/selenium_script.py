import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COOKIE_FILE = "leetcode_cookies.json"

def save_cookies(driver, path):
    with open(path, "w") as f:
        json.dump(driver.get_cookies(), f)

def load_cookies(driver, path):
    with open(path, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        if "sameSite" in cookie and cookie["sameSite"] == "None":
            cookie["sameSite"] = "Strict"
        driver.add_cookie(cookie)

def setup_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f"--user-data-dir={os.path.abspath('chrome-profile')}")
    return webdriver.Chrome(service=Service(), options=options)

def login_and_save_cookies(driver):
    print("🔑 Manual login required...")
    driver.get("https://leetcode.com/accounts/login/")
    print("⏳ Waiting for you to log in manually...")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'user')]"))
    )
    print("✅ Login successful, saving cookies...")
    save_cookies(driver, COOKIE_FILE)

def fetch_latest_submission(driver):
    print("📄 Navigating to submissions page...")
    driver.get("https://leetcode.com/submissions/")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/submissions/detail/')]")))
    
    print("📌 Opening latest submission...")
    latest = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    latest.click()
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ace_content")))
    code = driver.find_element(By.CLASS_NAME, "ace_content").text.strip()
    title = driver.title.split(" - ")[0].strip()
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    solution_dir = os.path.join(os.path.dirname(__file__), "../leetcode-solutions")
    os.makedirs(solution_dir, exist_ok=True)
    filename = f"{date_str}_{title.replace(' ', '_').replace('/', '_')}.txt"
    file_path = os.path.join(solution_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"✅ Code saved to: {file_path}")

if __name__ == "__main__":
    driver = setup_driver(headless=False)

    try:
        print("🌐 Connecting to LeetCode...")
        driver.get("https://leetcode.com")

        if os.path.exists(COOKIE_FILE):
            print("🍪 Found saved cookies. Attempting automatic login...")
            load_cookies(driver, COOKIE_FILE)
            driver.get("https://leetcode.com")
            time.sleep(3)

        # Check if user is logged in
        if not driver.get_cookies() or "LEETCODE_SESSION" not in [c['name'] for c in driver.get_cookies()]:
            login_and_save_cookies(driver)

        fetch_latest_submission(driver)

    except Exception as e:
        print("❌ Error occurred:", e)

    finally:
        driver.quit()
