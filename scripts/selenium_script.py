import os
import requests
from datetime import datetime

# 📦 Prepare headers using your LeetCode session cookie
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
if not LEETCODE_SESSION:
    raise Exception("❌ Missing LEETCODE_SESSION. Set it as a GitHub secret.")

HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION}",
    "User-Agent": "Mozilla/5.0"
}

# 🔍 GraphQL query to get latest accepted submission
query = {
    "query": """
    query {
      recentAcSubmissionList(limit: 1) {
        title
        titleSlug
        lang
        code
        timestamp
      }
    }
    """
}

print("🚀 Fetching your latest LeetCode submission...")

response = requests.post("https://leetcode.com/graphql", json=query, headers=HEADERS)
if response.status_code != 200:
    raise Exception(f"❌ Failed to fetch: {response.status_code} - {response.text}")

submission = response.json()["data"]["recentAcSubmissionList"][0]

title = submission["title"]
title_slug = submission["titleSlug"]
lang = submission["lang"].lower()
code = submission["code"]
timestamp = int(submission["timestamp"])

# 🧠 Convert to proper extension
ext_map = {
    "python": "py",
    "python3": "py",
    "java": "java",
    "cpp": "cpp",
    "c": "c",
    "javascript": "js",
    "typescript": "ts",
}
ext = ext_map.get(lang, "txt")

# 🧾 File naming
date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
filename_slug = title_slug.replace("-", "_")
filename = f"{date_str}_{filename_slug}.{ext}"
solution_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'leetcode-solutions'))
os.makedirs(solution_dir, exist_ok=True)
file_path = os.path.join(solution_dir, filename)

# 💾 Save code to file
with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"✅ Saved: {file_path}")

# 📝 Update README.md
readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
with open(readme_path, "w", encoding="utf-8") as readme:
    readme.write("# 🧠 Latest LeetCode Submission\n\n")
    readme.write(f"> 📌 [{title}](https://leetcode.com/problems/{title_slug}/)\n")
    readme.write(f"> 🗓️ **{date_str}**\n")
    readme.write(f"> 🧑‍💻 **Language**: `{lang}`\n\n")
    readme.write("```" + ext + "\n")
    readme.write(code[:1000])  # Limit preview to 1000 characters
    readme.write("\n```\n")

print(f"📄 README.md updated.")
