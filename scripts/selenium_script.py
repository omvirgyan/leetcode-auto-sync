# scripts/selenium_script.py

import os
import time
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Optional: LeetCode session cookie (set it in GitHub Secrets or locally)
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")

# Headless Chrome setup
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')

print("🚀 Launching browser...")
driver = uc.Chrome(options=options, headless=True)
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Set session cookie and login
    print("🔐 Navigating to LeetCode...")
    driver.get("https://leetcode.com")
    if LEETCODE_SESSION:
        print("🍪 Injecting session cookie...")
        driver.add_cookie({"name": "LEETCODE_SESSION", "value": LEETCODE_SESSION, "domain": ".leetcode.com", "path": "/"})
        driver.refresh()
        time.sleep(3)

    # Step 2: Navigate to submission page
    print("📄 Navigating to submissions...")
    driver.get("https://leetcode.com/submissions/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/submissions/detail/')]") ))

    print("📌 Opening latest submission...")
    latest_submission = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    submission_link = latest_submission.get_attribute("href")
    latest_submission.click()

    # Step 3: Extract title, code, language, and question link
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ace_content")))
    time.sleep(2)
    
    title = driver.title.split(" - ")[0].strip()
    filename_slug = title.replace(" ", "_").replace("/", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")

    code = driver.find_element(By.CLASS_NAME, "ace_content").text.strip()
    lang = driver.find_element(By.CLASS_NAME, "ant-select-selection-item").text.strip().lower()
    
    if "python" in lang:
        ext = ".py"
    elif "java" in lang:
        ext = ".java"
    else:
        ext = ".txt"

    # Question title and link
    question_anchor = driver.find_element(By.XPATH, "//div[@class='text-label-1 dark:text-dark-label-1 break-all text-base font-medium']/a")
    question_title = question_anchor.text.strip()
    question_url = question_anchor.get_attribute("href")

    # Step 4: Save solution file
    solution_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'leetcode-solutions'))
    os.makedirs(solution_dir, exist_ok=True)
    file_path = os.path.join(solution_dir, f"{date_str}_{filename_slug}{ext}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"✅ Saved: {file_path}")

    # Step 5: Update README.md
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
    with open(readme_path, "w", encoding="utf-8") as readme:
        readme.write("# 🧠 Latest LeetCode Submission\n\n")
        readme.write(f"> 📌 **{question_title}**\n")
        readme.write(f"> 🔗 [View Question]({question_url})\n")
        readme.write(f"> 🗓️ {date_str}\n")
        readme.write("\n---\n\n")
        readme.write(f"```{lang}\n")
        readme.write(code[:1000])
        readme.write("\n```\n")

    print(f"📄 README updated: {readme_path}")

except TimeoutException as te:
    print("❌ Timeout while waiting for an element:", te)
except NoSuchElementException as ne:
    print("❌ Element not found:", ne)
except Exception as e:
    print("❌ Error:", e)
finally:
    print("🧹 Closing browser...")
    driver.quit()
