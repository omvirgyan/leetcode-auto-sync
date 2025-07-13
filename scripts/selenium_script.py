from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time

options = Options()
# Use existing Chrome session
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Attach to running Chrome
driver = webdriver.Chrome(options=options)

try:
    print("🌐 Using existing Chrome session...")
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

    # Save code
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
