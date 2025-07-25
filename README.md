# 🧠 Latest LeetCode Submission

> 📌 **House Robber II**
> 📅 **2025-07-24**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/house-robber-ii/)

## ✅ Submitted Code

```java
class Solution {
    public int amountRob(int[] arr, int start, int end, int[] dp) {
        if(start > end) return 0;
        if(dp[start] != -1) return dp[start];
        int take = arr[start] + amountRob(arr, start + 2, end, dp);
        int skip = amountRob(arr, start + 1, end, dp);
        return dp[start] = Math.max(take, skip);
    }
    public int rob(int[] nums) {
        int n = nums.length;
        if(n == 1) return nums[0];
        int[] dp1 = new int[n];
        int[] dp2 = new int[n];
        Arrays.fill(dp1, -1);
        Arrays.fill(dp2, -1);
        int case1 = amountRob(nums, 0, n - 2, dp1); 
        int case2 = amountRob(nums, 1, n - 1, dp2);  
        return Math.max(case1, case2);
    }
}

```

<!-- Updated: 2025-07-25 07:12:48.631913 -->
