# 🧠 Latest LeetCode Submission

> 📌 **Excel Sheet Column Title**
> 📅 **2025-07-20**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/excel-sheet-column-title/)

## ✅ Submitted Code

```java
class Solution {
    public String convertToTitle(int columnNumber) {
        StringBuilder sb = new StringBuilder();
        while (columnNumber > 0) {
            columnNumber--;
            int rem = columnNumber % 26;
            sb.append((char)(rem + 'A'));
            columnNumber /= 26;
        }
        return sb.reverse().toString();
    }
}

```

<!-- Updated: 2025-07-20 19:59:05.215562 -->
