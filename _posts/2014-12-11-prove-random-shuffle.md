---
typora-root-url: ../
title: "洗牌算法 Random shuffle 证明"
categories: "mathematic"
tags: 
  - mathematic
---

洗牌算法 Random shuffle 证明

---

## 问题

洗牌算法，Random shuffle 算法，随机化序列

参考jdk1.8中`java.util.Collections`文件中`Collections.shuffle`代码：

```java
public static void shuffle(List<?> list, Random rnd) {
    int size = list.size();
    if (size < SHUFFLE_THRESHOLD || list instanceof RandomAccess) {
        for (int i=size; i>1; i--)
            swap(list, i-1, rnd.nextInt(i));
    } else {
        Object arr[] = list.toArray();

        // Shuffle array
        for (int i=size; i>1; i--)
            swap(arr, i-1, rnd.nextInt(i));

        // Dump array back into list
        // instead of using a raw type here, it's possible to capture
        // the wildcard but it will require a call to a supplementary
        // private method
        ListIterator it = list.listIterator();
        for (int i=0; i<arr.length; i++) {
            it.next();
            it.set(arr[i]);
        }
    }
}

public static void swap(List<?> list, int i, int j) {
    // instead of using a raw type here, it's possible to capture
    // the wildcard but it will require a call to a supplementary
    // private method
    final List l = list;
    l.set(i, l.set(j, l.get(i)));
}
```

简化关键代码如下：

```java
for (int i=size; i>1; i--)
    swap(list, i-1, rnd.nextInt(i));
```



其中`swap(list, i-1, rnd.nextInt(i));` 中 `rnd.nextInt(i)` 是产生 `[0, i-1]`中的一个随机整数。

可以用伪代码表达，对于数组` a[n]`操作`for i:=n to 1 do swap(a[i-1], a[random(0,i-1)]);`，其中`random(0,i-1)`为`[0, i-1]`中的一个随机整数。

## 问题的数学表述

某个数组 `a[:]`下标以0开始计数有n个元素，经过  `for i:=n to 1 do swap(a[i-1], a[random(0,i-1)]);` 操作后得到新的序列 `a[:]`，求证，第 a 个元素为原序列 x 的概率为 $p_{(i=x)}=\frac{1}{n}$

## 证明

采用数学归纳法证明

1. 当 $n = 2$ 时，显然成立，即 `for i:=2 to 1 do swap(a[i-1], a[random(0,i-1)]);` 操作，可以得出 $p_{(i = x)} = \frac{1}{2}$，对于 $i$ 在 $[1, 2]$ 内, $x$是序列 $a$ 的某一元素 成立
2. **假设** $n = k, (k >= 2)$ 成立，即 `for i:=k to 1 do swap(a[i-1], a[random(0,i-1)]);` 操作，可以得出 $p^{(k)}_{(i = x)} = \frac{1}{k}$，对于下标 $i$ 在 $[0, k-1]$ 内, $x$是序列 $a$ 的某一元素 成立；
   **则** $n = k + 1$ 时，操作 `for i:=k+1 to 1 do swap(a[i-1], a[random(0,i-1)]);`
   可分解为，先步骤1`swap(a[k], a[random(0, k)]);`，再步骤2 `for i:=k to 1 do swap(a[i-1], a[random(0, i-1)]); ` 两步操作，

    * 第一句伪代码执行得出：序列共k+1个元素，其中洗牌后第k个元素出现为原来的x概率记为 $$p^{(k+1)}_{(k = x)}$$ 其中 $$p^{(k+1)}_{(k = x)} = \frac{1}{k+1}$$， $x$ 是序列 $a$ 的某一元素，
    * 第二句伪代码执行得出：经过第一次步骤1的swap操作，a[0]到a[k-1]中出现原来元素a[k]的概率为$$\frac{k}{k+1}$$。后续步骤2中循环所得序列各个元素出现概率记为 $p^{(k+1)}_{(i = x)}$

      * 如果x是原来a[k]元素的话，即步骤1中a[k]与a[0] ~ a[k-1]交换了，并且后续步骤2中a[i]与a[k]换，$$p^{(k+1)}_{(i = x)} = p^{(k)}_{(i = x)} * \frac{k}{k+1} = \frac{1}{k} * \frac{k}{k+1} = \frac{1}{k+1}$$
      * 如果x是原来a[0]到a[k-1]中某元素的话，即步骤1中a[k]与a[0] ~ a[k-1]中除了x外某元素交换了，并且后续步骤2中a[i]与x换，$$p^{(k+1)}_{(i = x)} = \frac{1}{k} * \frac{k}{k+1} = \frac{1}{k+1}$$

      所以， $$p^{(k+1)}_{(i = x)} = \frac{1}{k+1}$$ ，即，对于 $n = k + 1$, $$p_{(i = x)} = \frac{1}{k+1}$$

综上，由1，2得 $p_{(i = x)} = \frac{1}{n}$ 成立，问题得证

