import os
import requests
from datetime import datetime

# Load secrets from environment
SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN = os.getenv("LEETCODE_CSRF")
USERNAME = "Omvirgyan"

if not SESSION or not CSRF_TOKEN:
    raise Exception("❌ LEETCODE_SESSION or LEETCODE_CSRF is missing")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "X-CSRFToken": CSRF_TOKEN,
    "cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN};"
}

# Step 1: Fetch metadata using GraphQL
print("📡 Fetching latest accepted submission...")
res = requests.post(
    "https://leetcode.com/graphql",
    json={
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
    },
    headers=HEADERS
)

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

# Step 2: Fetch code from submissions dump
print("📥 Fetching submitted code...")
submission_dump_url = f"https://leetcode.com/api/submissions/{slug}/"
resp = requests.get(submission_dump_url, headers=HEADERS)
json_data = resp.json()

submission_list = json_data.get("submissions_dump", [])
ac_submission = next((s for s in submission_list if s["status_display"] == "Accepted"), None)

if not ac_submission or "code" not in ac_submission:
    raise Exception("❌ Accepted submission with code not found")

code = ac_submission["code"]

# Step 3: Write everything to README
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_path = os.path.join(project_root, 'README.md')

print(f"📝 Writing to README.md at: {readme_path}")
with open(readme_path, 'w', encoding='utf-8') as readme:
    readme.write("# 🧠 Latest LeetCode Submission\n\n")
    readme.write(f"> 📌 **{title}**\n")
    readme.write(f"> 📅 **{date}**\n")
    readme.write(f"> 💻 **Language:** `{lang}`\n")
    readme.write(f"> 🔗 [Problem Link]({problem_url})\n\n")
    readme.write("## ✅ Submitted Code\n\n")
    readme.write(f"```{lang.lower()}\n{code}\n```\n")
    readme.write(f"\n<!-- Updated: {datetime.now()} -->\n")

print("✅ README.md updated successfully.")
print(f"🔗 Problem: {problem_url}")
