import os
from datetime import datetime

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
wait = WebDriverWait(driver, 15)

try:
    print("🚀 Opening LeetCode login page...")
    driver.get("https://leetcode.com/accounts/login/")

    # ✅ Wait for login fields to be present
    print("⏳ Waiting for login form...")
    wait.until(EC.presence_of_element_located((By.ID, "id_login"))).send_keys(USERNAME)
    driver.find_element(By.ID, "id_password").send_keys(PASSWORD)
    driver.find_element(By.ID, "signin_btn").click()
    print("🔓 Login submitted.")

    # ✅ Wait for submissions page after login
    print("📄 Navigating to submissions...")
    driver.get("https://leetcode.com/submissions/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/submissions/detail/')]")))

    print("📌 Opening most recent submission...")
    latest_submission = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    latest_submission.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ace_content")))

    title = driver.title.split(" - ")[0].strip()
    filename_slug = title.replace(" ", "_").replace("/", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")
    code = driver.find_element(By.CLASS_NAME, "ace_content").text.strip()

    # Save the solution
    solution_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'leetcode-solutions'))
    os.makedirs(solution_dir, exist_ok=True)
    file_path = os.path.join(solution_dir, f"{date_str}_{filename_slug}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    # Update README.md
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
    with open(readme_path, "w", encoding="utf-8") as readme:
        readme.write("# 🧠 Latest LeetCode Submission\n\n")
        readme.write(f"> 📌 **{title}**\n")
        readme.write(f"> 🗓️ **{date_str}**\n")
        readme.write("> 🧑‍💻 **Solution**\n\n")
        readme.write("```java\n")
        readme.write(code[:1000])  # Preview only first 1000 chars
        readme.write("\n```\n")

    print(f"✅ Solution saved to: {file_path}")
    print(f"📄 README updated at: {readme_path}")

except TimeoutException as te:
    print("❌ Timeout waiting for an element to load.")
    print(te)
except NoSuchElementException as ne:
    print("❌ Couldn't locate an expected element.")
    print(ne)
except Exception as e:
    print("❌ Unexpected error occurred.")
    print(e)
finally:
    print("🧹 Closing browser...")
    driver.quit()
