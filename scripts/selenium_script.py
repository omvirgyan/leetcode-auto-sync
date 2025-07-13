import os
from datetime import datetime
import time

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# 🔐 Load credentials
USERNAME = os.getenv("LEETCODE_USER")
PASSWORD = os.getenv("LEETCODE_PASS")

if not USERNAME or not PASSWORD:
    raise Exception("❌ Missing LeetCode credentials. Please set LEETCODE_USER and LEETCODE_PASS.")

# 🌐 Headless browser setup
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

try:
    print("🚀 Opening LeetCode login page...")
    driver.get("https://leetcode.com/accounts/login/")

    # ✅ Wait for login form fields
    print("⏳ Waiting for login fields...")
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "login")))
    username_input.clear()
    username_input.send_keys(USERNAME)

    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.clear()
    password_input.send_keys(PASSWORD)

    wait.until(EC.element_to_be_clickable((By.ID, "signin_btn"))).click()
    print("🔓 Login submitted!")

    # ✅ Navigate to submissions
    print("📄 Navigating to submissions page...")
    driver.get("https://leetcode.com/submissions/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/submissions/detail/')]")))

    print("📌 Opening most recent submission...")
    latest_submission = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    submission_url = latest_submission.get_attribute("href")
    driver.get(submission_url)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ace_content")))
    time.sleep(1)  # Sometimes needed for Monaco editor

    # ✅ Extract info
    print("🧠 Fetching solution data...")
    title_element = driver.find_element(By.XPATH, "//div[contains(@class,'css-v3d350')]")
    title = title_element.text.strip()

    code_element = driver.find_element(By.CLASS_NAME, "ace_content")
    code = code_element.text.strip()

    lang_element = driver.find_element(By.XPATH, "//span[contains(text(),'Language')]/following-sibling::div")
    language = lang_element.text.strip().lower()

    # 🧠 Detect file extension
    ext = {
        "python": "py",
        "python3": "py",
        "java": "java",
        "c++": "cpp",
        "c": "c",
        "javascript": "js"
    }.get(language, "txt")

    filename_slug = title.replace(" ", "_").replace("/", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{filename_slug}.{ext}"

    # 📁 Save to file
    solution_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'leetcode-solutions'))
    os.makedirs(solution_dir, exist_ok=True)
    file_path = os.path.join(solution_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    # 📝 Update README
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
    with open(readme_path, "w", encoding="utf-8") as readme:
        readme.write("# 🧠 Latest LeetCode Submission\n\n")
        readme.write(f"> 📌 **[{title}]({submission_url})**\n")
        readme.write(f"> 🗓️ **{date_str}**\n")
        readme.write(f"> 💻 **Language:** `{language}`\n\n")
        readme.write("```" + ext + "\n")
        readme.write(code[:1000])  # Limit preview to first 1000 characters
        readme.write("\n```\n")

    print(f"✅ Saved: {file_path}")
    print(f"📄 Updated: {readme_path}")
    print(f"🔗 Problem Link: {submission_url}")

except TimeoutException as te:
    print("❌ Timeout waiting for an element.")
    print(te)
except NoSuchElementException as ne:
    print("❌ Element not found.")
    print(ne)
except Exception as e:
    print("❌ Unexpected error.")
    print(e)
finally:
    print("🧹 Closing browser...")
    driver.quit()
