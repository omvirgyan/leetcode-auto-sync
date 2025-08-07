# 🧠 Latest LeetCode Submission

> 📌 **Longest Increasing Subsequence**
> 📅 **2025-08-06**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/longest-increasing-subsequence/)

## ✅ Submitted Code

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        if (nums.length == 0) return 0;

        int[] dp = new int[nums.length];
        dp[0] = 1;
        int ans = 1;

        for (int i = 1; i < dp.length; i++) {
            int max = 0;
            for (int j = 0; j < i; j++) {
                if (nums[i] > nums[j]) { 
                    max = Math.max(max, dp[j]);
                }
            }
            dp[i] = max + 1;
            ans = Math.max(ans, dp[i]);
        }

        return ans;
    }
}

```

<!-- Updated: 2025-08-07 17:59:08.578943 -->
