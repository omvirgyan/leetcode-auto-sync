import requests
import os
from datetime import datetime

USERNAME = "Omvirgyan"  # Replace with your LeetCode username
README_PATH = "README.md"

# GraphQL query to get recent submissions
query = {
    "operationName": "recentSubmissionList",
    "variables": {"username": USERNAME},
    "query": """
        query recentSubmissionList($username: String!) {
          recentSubmissionList(username: $username) {
            title
            titleSlug
            status
            lang
            time
          }
        }
    """
}

headers = {
    "Content-Type": "application/json",
    "Referer": f"https://leetcode.com/{USERNAME}/",
    "Origin": "https://leetcode.com",
}

response = requests.post("https://leetcode.com/graphql", json=query, headers=headers)
data = response.json()

try:
    recent = data["data"]["recentSubmissionList"][0]  # Get the latest submission

    title = recent["title"]
    slug = recent["titleSlug"]
    lang = recent["lang"]
    timestamp = datetime.fromtimestamp(recent["time"]).strftime("%Y-%m-%d %H:%M:%S")
    link = f"https://leetcode.com/problems/{slug}/"

    # Update README.md
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write("# 🧠 Latest LeetCode Submission\n\n")
        f.write(f"> 📌 **{title}**\n")
        f.write(f"> 🗓️ **{timestamp}**\n")
        f.write(f"> 🧑\u200d💻 **Language**: {lang}\n")
        f.write(f"> 🔗 [Problem Link]({link})\n")

    print(f"✅ Updated README.md with latest submission: {title}")

except Exception as e:
    print("❌ Failed to fetch or update submission info.")
    print(e)
