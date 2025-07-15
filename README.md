# 🧠 Latest LeetCode Submission

> 📌 **Fibonacci Number**
> 📅 **2025-07-15**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/fibonacci-number/)

## ✅ Submitted Code

```java
class Solution {
   public int fibByDp(int n,int arr[]){
    if(n==0 || n==1) return n;
    if(arr[n]!=-1) return arr[n];
    arr[n]=fibByDp(n-1,arr) + fibByDp(n-2,arr);
    return arr[n];
   }

    public int fib(int n) {
    int[] arr=new int[n+1];
    Arrays.fill(arr,-1);
    int ans =fibByDp(n,arr);
    return ans;
        
    }
}
```

<!-- Updated: 2025-07-15 17:40:40.873320 -->
