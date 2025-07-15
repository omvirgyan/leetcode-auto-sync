# 🧠 Latest LeetCode Submission

> 📌 **Pascal's Triangle II**
> 📅 **2025-07-14**
> 💻 **Language:** `java`
> 🔗 [Problem Link](https://leetcode.com/problems/pascals-triangle-ii/)

## ✅ Submitted Code

```java
import java.util.*;

class Solution {
    public List<Integer> getRow(int rowIndex) {
        List<Integer> row = new ArrayList<>();
        row.add(1);
        for (int i = 1; i <= rowIndex; i++) {
            for (int j = row.size() - 1; j >= 1; j--) {
                row.set(j, row.get(j) + row.get(j - 1));
            }
            row.add(1); // last element is always 1
        }
        
        return row;
    }
}

```

<!-- Updated: 2025-07-15 15:20:57.024929 -->
