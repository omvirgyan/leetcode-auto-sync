# 🧠 Latest LeetCode Submission

> 📌 **Count Square Submatrices with All Ones**
> 📅 **2025-07-25**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/count-square-submatrices-with-all-ones/)

## ✅ Submitted Code

```java
class Solution {
    public int countSquares(int[][] matrix) {
         int m = matrix.length;
        int n = matrix[0].length;
        int count=0;
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
              if(matrix[i][j]==0) continue;
              if(i>0 && j>0){
                matrix[i][j] +=min(matrix[i-1][j],matrix[i][j-1],matrix[i-1][j-1]);
              }
              count +=matrix[i][j];
            }
        }
        return count;
    }
    public static int  min(int a,int b,int c){
        return Math.min(a,Math.min(b,c));
    }
}
```

<!-- Updated: 2025-07-26 05:12:42.474535 -->
