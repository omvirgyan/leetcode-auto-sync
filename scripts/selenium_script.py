import os
import time
from datetime import datetime

# ✅ Auto-install matching ChromeDriver
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# 🔐 Read secure credentials
USERNAME = os.getenv("LEETCODE_USER")
PASSWORD = os.getenv("LEETCODE_PASS")

if not USERNAME or not PASSWORD:
    raise Exception("❌ Missing LEETCODE_USER or LEETCODE_PASS environment variables.")

# 🌐 Configure Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

print("🚀 Starting headless browser...")
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Open login page
    print("🔐 Navigating to login page...")
    driver.get("https://leetcode.com/accounts/login/")
    time.sleep(4)

    # Step 2: Enter credentials using correct IDs
    print("✏️ Entering login credentials...")
    driver.find_element(By.ID, "id_login").send_keys(USERNAME)
    driver.find_element(By.ID, "id_password").send_keys(PASSWORD)
    driver.find_element(By.ID, "signin_btn").click()
    time.sleep(6)

    # Step 3: Navigate to submissions
    print("📄 Opening submissions page...")
    driver.get("https://leetcode.com/submissions/")
    time.sleep(5)

    # Step 4: Click the latest submission
    print("🔎 Fetching latest submission...")
    latest_submission = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    latest_submission.click()
    time.sleep(4)

    # Step 5: Extract problem title
    title = driver.title.split(" - ")[0].strip()
    filename_slug = title.replace(" ", "_").replace("/", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Step 6: Extract code from Monaco editor
    print("📥 Extracting code...")
    code_element = driver.find_element(By.CLASS_NAME, "ace_content")
    code = code_element.text.strip()

    # Step 7: Save code to file
    solution_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'leetcode-solutions'))
    os.makedirs(solution_dir, exist_ok=True)
    file_path = os.path.join(solution_dir, f"{date_str}_{filename_slug}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    # Step 8: Update README
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
    with open(readme_path, "w", encoding="utf-8") as readme:
        readme.write("# 🧠 Latest LeetCode Submission\n\n")
        readme.write(f"> 📌 **{title}**\n")
        readme.write(f"> 🗓️ **{date_str}**\n")
        readme.write("> 🧑‍💻 **Solution**\n\n")
        readme.write("```java\n")
        readme.write(code[:1000])  # Truncate preview
        readme.write("\n```\n")

    print(f"✅ Saved solution: {file_path}")
    print(f"📄 Updated README.md successfully.")

except NoSuchElementException as e:
    print("❌ Element not found. Check selector or page structure.")
    print(e)
except WebDriverException as e:
    print("❌ WebDriver error occurred.")
    print(e)
except Exception as e:
    print("❌ Unexpected error occurred.")
    print(e)
finally:
    print("🧹 Closing browser...")
    driver.quit()
