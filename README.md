# 🧠 Latest LeetCode Submission

> 📌 **Min Cost Climbing Stairs**
> 📅 **2025-07-15**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/min-cost-climbing-stairs/)

## ✅ Submitted Code

```java
public class Solution {
    public int minCost(int[] cost, int idx, int[] dp) {
        if(idx == 0 || idx == 1) return cost[idx];
        if(dp[idx] != -1) return dp[idx];
        return dp[idx] = cost[idx] + Math.min(minCost(cost, idx - 1, dp), minCost(cost, idx - 2, dp));
    }

    public int minCostClimbingStairs(int[] cost) {
        int n = cost.length;
        int[] dp = new int[n];
        Arrays.fill(dp, -1);
        return Math.min(minCost(cost, n - 1, dp), minCost(cost, n - 2, dp));
    }
}

```

<!-- Updated: 2025-07-16 19:33:46.571153 -->
