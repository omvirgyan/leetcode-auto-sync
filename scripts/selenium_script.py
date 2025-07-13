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

submission = data["data"]["recentAcSubmissionList"][0]
title = submission["title"]
slug = submission["titleSlug"]
lang = submission["lang"]
ts = int(submission["timestamp"])
date = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
problem_url = f"https://leetcode.com/problems/{slug}/"

print(f"✅ Fetched: {title} ({lang})")

# Fetch solution code
solution_url = f"https://leetcode.com/graphql"
solution_payload = {
    "operationName": "mySubmissionDetail",
    "variables": {
        "submissionId": None  # Cannot fetch exact code without ID
    },
    "query": """
    query mySubmissionDetail($submissionId: ID!) {
      submissionDetail(submissionId: $submissionId) {
        code
        lang
      }
    }
    """
}

print("⚠️ Note: This method fetches metadata only (title, lang, link). Code content requires browser automation or ID access.")
print(f"🔗 Problem: {problem_url}")
