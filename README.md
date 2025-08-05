# 🧠 Latest LeetCode Submission

> 📌 **N-Repeated Element in Size 2N Array**
> 📅 **2025-08-04**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/n-repeated-element-in-size-2n-array/)

## ✅ Submitted Code

```java
class Solution {
    public int repeatedNTimes(int[] nums) {
        HashMap<Integer,Integer> map=new HashMap<>();
        for(int i=0;i<nums.length;i++){
            map.put(nums[i],map.getOrDefault(nums[i],0)+1);
            if(map.get(nums[i])>1) return nums[i];
        }
        return 0;
    }
}
```

<!-- Updated: 2025-08-05 06:15:21.347486 -->
