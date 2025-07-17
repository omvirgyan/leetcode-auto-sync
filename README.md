# 🧠 Latest LeetCode Submission

> 📌 **Jump Game**
> 📅 **2025-07-16**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/jump-game/)

## ✅ Submitted Code

```java
public class Solution {
    public boolean canJump(int[] nums) {
        int maxReach = 0; 
        for (int i = 0; i < nums.length; i++) {
            if (i > maxReach) {
                return false;  
            }
            maxReach = Math.max(maxReach, i + nums[i]);  
           
        }
        return true;
    }
}
```

<!-- Updated: 2025-07-17 05:59:08.204758 -->
