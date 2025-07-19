# 🧠 Latest LeetCode Submission

> 📌 **House Robber**
> 📅 **2025-07-18**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/house-robber/)

## ✅ Submitted Code

```java
class Solution {
    public int amountRob(int[] arr,int idx,int[] dp){
        if(idx>=arr.length) return 0;
        if(dp[idx]!=-1)return dp[idx];
        int take=arr[idx]+ amountRob(arr,idx+2,dp);
        int skip=amountRob(arr,idx+1,dp);
        
        return dp[idx]=Math.max(take,skip);
    }
    public int rob(int[] nums) {
       int [] dp=new int[nums.length];
       Arrays.fill(dp,-1);
       return amountRob(nums,0,dp);
    }
}
```

<!-- Updated: 2025-07-19 05:59:24.835853 -->
