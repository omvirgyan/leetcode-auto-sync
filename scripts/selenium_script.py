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

    print("⏳ Waiting for login fields...")
    wait.until(EC.presence_of_element_located((By.ID, "id_login"))).send_keys(USERNAME)
    driver.find_element(By.ID, "id_password").send_keys(PASSWORD)
    driver.find_element(By.ID, "signin_btn").click()
    print("🔓 Login submitted!")

    print("📄 Navigating to submissions page...")
    driver.get("https://leetcode.com/submissions/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/submissions/detail/')]")))

    print("📌 Opening latest submission...")
    latest_submission = driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]")
    submission_url = latest_submission.get_attribute("href")
    latest_submission.click()

    print("🧠 Waiting for code editor to load...")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ace_content")))

    # 🧾 Problem title and slug
    title_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/problems/')]")))
    problem_title = title_element.text.strip()
    problem_link = title_element.get_attribute("href")

    # 🧠 Detect language
    lang_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ant-select-selection-item")))
    language = lang_element.text.strip().lower()

    # 🧩 Language-to-extension mapping
    ext_map = {
        "python": "py",
        "python3": "py",
        "java": "java",
        "cpp": "cpp",
        "c++": "cpp",
        "c": "c",
        "javascript": "js",
        "typescript": "ts",
        "c#": "cs",
        "golang": "go",
        "ruby": "rb",
        "swift": "swift",
        "kotlin": "kt",
        "rust": "rs"
    }
    file_ext = ext_map.get(language, "txt")

    # 🧾 Extract code lines from Monaco editor
    editor = driver.find_element(By.CLASS_NAME, "ace_content")
    lines = editor.find_elements(By.CSS_SELECTOR, ".ace_line")
    code = "\n".join(line.text for line in lines if line.text.strip())

    if not code:
        raise Exception("❌ Code extraction failed! No code lines found.")

    # 📁 Save solution file
    filename_slug = problem_title.replace(" ", "_").replace("/", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")
    solution_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'leetcode-solutions'))
    os.makedirs(solution_dir, exist_ok=True)
    file_path = os.path.join(solution_dir, f"{date_str}_{filename_slug}.{file_ext}")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    # 📄 Generate README.md preview
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
    with open(readme_path, "w", encoding="utf-8") as readme:
        readme.write("# 🧠 Latest LeetCode Submission\n\n")
        readme.write(f"> 📌 **[{problem_title}]({problem_link})**\n")
        readme.write(f"> 🗓️ **{date_str}**\n")
        readme.write(f"> 💻 **Language**: `{language}`\n\n")
        readme.write(f"```{file_ext}\n")
        readme.write(code[:1000])  # Limit preview
        readme.write("\n```\n")

    # ✅ Print useful debug info
    print("✅ Submission fetched successfully:")
    print(f"🔖 Title: {problem_title}")
    print(f"🔗 Link: {problem_link}")
    print(f"💻 Language: {language}")
    print(f"📁 Saved at: {file_path}")
    print("📄 Code preview:")
    print("-" * 40)
    print("\n".join(code.splitlines()[:10]))  # print first 10 lines
    print("... (truncated)")
    print("-" * 40)

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
