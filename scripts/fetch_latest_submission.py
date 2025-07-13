import os
import requests
from datetime import datetime

# Load secrets from environment
SESSION = os.getenv("LEETCODE_SESSION")
CSRF_TOKEN = os.getenv("LEETCODE_CSRF")

if not SESSION or not CSRF_TOKEN:
    raise Exception("❌ LEETCODE_SESSION or LEETCODE_CSRF is missing")

# LeetCode GraphQL endpoint
URL = "https://leetcode.com/graphql"

# Headers with session and csrf token
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "X-CSRFToken": CSRF_TOKEN,
    "cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF_TOKEN};"
}

# Query to get recent AC submissions
QUERY = {
    "operationName": "recentAcSubmissions",
    "variables": {"username": "Omvirgyan"},
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
res = requests.post(URL, json=QUERY, headers=HEADERS)
data = res.json()

if not data.get("data") or not data["data"].get("recentAcSubmissionList"):
    raise Exception("❌ No recent accepted submissions found")

submission = data["data"]["recentAcSubmissionList"][0]
title = submission["title"]
slug = submission["titleSlug"]
lang = submission["lang"]
ts = int(submission["timestamp"])
date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
problem_url = f"https://leetcode.com/problems/{slug}/"

print(f"✅ Fetched: {title} ({lang})")

# Save minimal solution info to README
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_path = os.path.join(project_root, 'README.md')

print(f"📝 Writing to README.md at: {readme_path}")
with open(readme_path, 'w', encoding='utf-8') as readme:
    readme.write("# 🧠 Latest LeetCode Submission\n\n")
    readme.write(f"> 📌 **{title}**\n")
    readme.write(f"> 📅 **{date}**\n")
    readme.write(f"> 💻 **Language:** `{lang}`\n")
    readme.write(f"> 🔗 [Problem Link]({problem_url})\n")
    readme.write(f"\n<!-- Updated: {datetime.now()} -->\n")

print("✅ README.md updated successfully.")
print(f"🔗 Problem: {problem_url}")

# 🚫 NOTE: Code content requires browser automation or submission ID, which this script does not handle.
