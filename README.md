# 🧠 Latest LeetCode Submission

> 📌 **Longest Subarray With Maximum Bitwise AND**
> 📅 **2025-08-01**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/longest-subarray-with-maximum-bitwise-and/)

## ✅ Submitted Code

```java
class Solution {
    public int longestSubarray(int[] nums) {
        int max = 0;
        for (int num : nums) {
            max = Math.max(max, num);
        }
        int maxLen = 0, currentLen = 0;
        for (int num : nums) {
            if (num == max) {
                currentLen++;
                maxLen = Math.max(maxLen, currentLen);
            } else {
                currentLen = 0;
            }
        }

        return maxLen;
    }
}

```

<!-- Updated: 2025-08-01 19:09:26.028354 -->
