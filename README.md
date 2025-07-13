readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
with open(readme_path, "w", encoding="utf-8") as readme:
    readme.write("# 🧠 Latest LeetCode Submission\n\n")
    readme.write(f"> 📌 **{title}**\n")
    readme.write(f"> 📅 **{date}**\n")
    readme.write(f"> 💻 **Language:** `{lang}`\n")
    readme.write(f"> 🔗 [Problem Link]({problem_url})\n")
