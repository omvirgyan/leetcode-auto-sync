# 🧠 Latest LeetCode Submission

> 📌 **Unique Paths**
> 📅 **2025-07-21**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/unique-paths/)

## ✅ Submitted Code

```java
class Solution {
    public int pathCount(int i, int j, int m, int n,int[][] dp) {
        if (i == m - 1 && j == n - 1)
            return 1;
        if (i >= m || j >= n)
            return 0;
        if(dp[i][j]!=-1) return dp[i][j];
        int right = pathCount(i, j + 1, m, n,dp);
        int down = pathCount(i + 1, j, m, n,dp);
        dp[i][j]=right + down;
         return dp[i][j];
    }

    public int uniquePaths(int m, int n) {
        int[][] dp = new int[m + 1][n + 1];
        for (int[] row : dp) {
            Arrays.fill(row, -1);
        }
        return pathCount(0, 0, m, n,dp);
    }
}

```

<!-- Updated: 2025-07-22 03:21:58.269200 -->
