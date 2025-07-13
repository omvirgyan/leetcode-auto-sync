import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Connect to existing Chrome (already running with --remote-debugging-port)
options = Options()
options.debugger_address = "127.0.0.1:9222"

try:
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 60)

    print("🌐 Connected to existing Chrome session.")
    driver.get("https://leetcode.com")

    # 🔍 Check if already logged in by waiting for user icon
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nav-user-icon")))
        print("✅ Already logged in to LeetCode.")
    except:
        print("🔐 Not logged in. Redirecting to login page...")
        driver.get("https://leetcode.com/accounts/login/")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nav-user-icon")))
        print("✅ Manual login completed.")

    # ✅ Navigate to submissions page
    print("📄 Navigating to submissions...")
    driver.get("https://leetcode.com/submissions/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/submissions/detail/')]")))

    # ✅ Open the latest submission
    print("📌 Opening latest submission...")
    latest = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    latest.click()

    # ✅ Extract code from editor
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ace_content")))
    code = driver.find_element(By.CLASS_NAME, "ace_content").text.strip()
    title = driver.title.split(" - ")[0].strip()
    date_str = datetime.now().strftime("%Y-%m-%d")

    # ✅ Save solution to file
    filename = f"{date_str}_{title.replace(' ', '_').replace('/', '_')}.txt"
    solution_dir = os.path.join(os.path.dirname(__file__), "leetcode-solutions")
    os.makedirs(solution_dir, exist_ok=True)
    file_path = os.path.join(solution_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"✅ Code saved to: {file_path}")

except Exception as e:
    print("❌ Error occurred:", e)

finally:
    input("🔚 Press Enter to exit (browser will remain open)...")
