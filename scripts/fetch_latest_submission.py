import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# Load secrets from environment
SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN = os.getenv("LEETCODE_CSRF")
USERNAME = "Omvirgyan"

if not SESSION or not CSRF_TOKEN:
    raise Exception("❌ LEETCODE_SESSION or LEETCODE_CSRF is missing")

# LeetCode GraphQL endpoint
GRAPHQL_URL = "https://leetcode.com/graphql"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "X-CSRFToken": CSRF_TOKEN,
    "cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN};"
}

# 1️⃣ Get latest accepted submission info
QUERY = {
    "operationName": "recentAcSubmissions",
    "variables": {"username": USERNAME},
    "query": """
    query recentAcSubmissions($username: String!) {
      recentAcSubmissionList(username: $username) {
        title
        titleSlug
        timestamp
        lang
      }
    }
    """
}

print("📡 Fetching latest accepted submission...")
res = requests.post(GRAPHQL_URL, json=QUERY, headers=HEADERS)
data = res.json()

subs = data.get("data", {}).get("recentAcSubmissionList", [])
if not subs:
    raise Exception("❌ No recent accepted submissions found")

submission = subs[0]
title = submission["title"]
slug = submission["titleSlug"]
lang = submission["lang"]
ts = int(submission["timestamp"])
date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
problem_url = f"https://leetcode.com/problems/{slug}/"

print(f"✅ Fetched: {title} ({lang})")

# 2️⃣ Scrape code from submission page (latest submissions)
submissions_url = f"https://leetcode.com/api/submissions/{slug}"
resp = requests.get(submissions_url, headers=HEADERS)
json_data = resp.json()

submission_list = json_data.get("submissions_dump", [])
if not submission_list:
    raise Exception("❌ No submissions found in dump")

# Filter AC submissions and get latest one
ac_submission = next((s for s in submission_list if s["status_display"] == "Accepted"), None)
if not ac_submission:
    raise Exception("❌ No Accepted submission found")

code = ac_submission["code"]
lang = ac_submission["lang"]
timestamp = ac_submission["timestamp"]
date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

# 3️⃣ Write to README.md
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_path = os.path.join(project_root, 'README.md')

print(f"📝 Writing to README.md at: {readme_path}")
with open(readme_path, 'w', encoding='utf-8') as readme:
    readme.write("# 🧠 Latest LeetCode Submission\n\n")
    readme.write(f"> 📌 **{title}**\n")
    readme.write(f"> 📅 **{date}**\n")
    readme.write(f"> 💻 **Language:** `{lang}`\n")
    readme.write(f"> 🔗 [Problem Link]({problem_url})\n\n")
    readme.write("## 🧾 Submitted Code\n\n")
    readme.write(f"```{lang.lower()}\n{code}\n```\n")
    readme.write(f"\n<!-- Updated: {datetime.now()} -->\n")

print("✅ README.md updated successfully.")
print(f"🔗 Problem: {problem_url}")
