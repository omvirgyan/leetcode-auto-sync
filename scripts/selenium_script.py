# scripts/selenium_script.py

import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Read credentials from environment (secure)
USERNAME = os.getenv("LEETCODE_USER")
PASSWORD = os.getenv("LEETCODE_PASS")

if not USERNAME or not PASSWORD:
    raise Exception("❌ Missing LeetCode credentials. Please set LEETCODE_USER and LEETCODE_PASS.")

# Set up headless Chrome browser
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Log in to LeetCode
    driver.get("https://leetcode.com/accounts/login/")
    time.sleep(3)
    driver.find_element(By.ID, "id_login").send_keys(USERNAME)
    driver.find_element(By.ID, "id_password").send_keys(PASSWORD)
    driver.find_element(By.ID, "signin_btn").click()
    time.sleep(5)

    # Step 2: Go to submission page
    driver.get("https://leetcode.com/submissions/")
    time.sleep(5)

    # Step 3: Click on the most recent submission link
    latest_submission = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    latest_submission.click()
    time.sleep(4)

    # Step 4: Extract title and code
    title = driver.title.split(" - ")[0].strip()
    filename_slug = title.replace(" ", "_").replace("/", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")

    code_element = driver.find_element(By.CLASS_NAME, "ace_content")
    code = code_element.text.strip()

    # Step 5: Save solution to file
    solution_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'leetcode-solutions'))
    os.makedirs(solution_dir, exist_ok=True)
    file_path = os.path.join(solution_dir, f"{date_str}_{filename_slug}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    # Step 6: Generate README.md
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
    with open(readme_path, "w", encoding="utf-8") as readme:
        readme.write("# 🧠 Latest LeetCode Submission\n\n")
        readme.write(f"> 📌 **{title}**\n")
        readme.write(f"> 🗓️ **{date_str}**\n")
        readme.write("> 🧑‍💻 **Solution**\n\n")
        readme.write("```java\n")
        readme.write(code[:1000])  # truncate to avoid overflowing GitHub preview
        readme.write("\n```\n")

    print(f"✅ Latest solution saved to: {file_path}")
    print(f"📄 README updated successfully.")

finally:
    driver.quit()
