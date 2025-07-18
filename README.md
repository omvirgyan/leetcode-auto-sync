# 🧠 Latest LeetCode Submission

> 📌 **N-th Tribonacci Number**
> 📅 **2025-07-18**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/n-th-tribonacci-number/)

## ✅ Submitted Code

```java
class Solution {
    public int tribonacci(int n) {
        if(n==0||n==1) return n;
        if(n==2) return 1;
        int[] dp=new int[n+1];
        dp[0]=0;
        dp[1]=1;
        dp[2]=1;
        for(int i=3;i<=n;i++){
            dp[i]=dp[i-1]+dp[i-2]+dp[i-3];
        }
        return dp[n];
    }
}
```

<!-- Updated: 2025-07-18 14:09:58.025932 -->
