# selenium_script.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, os

USERNAME = os.getenv("LEETCODE_USER")
PASSWORD = os.getenv("LEETCODE_PASS")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://leetcode.com/accounts/login/")
time.sleep(3)
driver.find_element(By.ID, "id_login").send_keys(USERNAME)
driver.find_element(By.ID, "id_password").send_keys(PASSWORD)
driver.find_element(By.ID, "signin_btn").click()
time.sleep(5)

driver.get("https://leetcode.com/submissions/")
time.sleep(5)
driver.find_element(By.XPATH, "//a[contains(@href, '/submissions/detail/')]").click()
time.sleep(4)

title = driver.title.split(" - ")[0].strip()
filename_slug = title.replace(" ", "_")
code_element = driver.find_element(By.CLASS_NAME, "ace_content")
code = code_element.text

date_str = time.strftime("%Y-%m-%d")
file_path = f"../leetcode-solutions/{date_str}_{filename_slug}.txt"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

# Update README section
readme_path = "../README.md"
with open(readme_path, "w", encoding="utf-8") as readme:
    readme.write(f"# 🧠 Latest LeetCode Submission\n\n")
    readme.write(f"> 📌 **{title}**\n")
    readme.write(f"> 🗓️ **{date_str}**\n")
    readme.write(f"> 🧑‍💻 **Solution**\n\n")
    readme.write("```java\n")
    readme.write(code[:1000])  # truncate if too long
    readme.write("\n```\n")

print(f"✅ Latest solution saved to: {file_path} and README updated.")
driver.quit()
