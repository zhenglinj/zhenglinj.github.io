---
typora-root-url: ../
title: "常用排序算法介绍"
categories: "technology"
tags: [sorting, technology]
---


排序算法简单讲解

---

## 图说排序

> [7 种常用的排序算法](http://blog.jobbole.com/11745/)  

## 具体介绍

> [冒泡排序 Bubble sort](http://www.cnblogs.com/morewindows/archive/2011/08/06/2129603.html)  
> [插入排序 Insertion sort](http://www.cnblogs.com/morewindows/archive/2011/08/06/2129610.html)  
> [希尔排序 Shell sort](http://www.cnblogs.com/morewindows/archive/2011/08/08/2130684.html)  
> [选择排序 Selection sort](http://www.cnblogs.com/morewindows/archive/2011/08/09/2131953.html)  
> [归并排序 Merge sort](http://www.cnblogs.com/morewindows/archive/2011/08/11/2134593.html)  
> [快速排序 Quick sort](http://www.cnblogs.com/morewindows/archive/2011/08/13/2137415.html)  
> [堆排序   Heap sort](http://www.cnblogs.com/morewindows/archive/2011/08/22/2149612.html)  

## 复杂度比较

[zh.Wikipedia](https://zh.wikipedia.org/wiki/%E6%8E%92%E5%BA%8F%E7%AE%97%E6%B3%95)  
[en.Wikipedia](https://en.wikipedia.org/wiki/Sorting_algorithm)  

| 排序法 | 稳定度 | 平均时间         | 最差情形          | 额外空间       | 备注                          |
|--------|--------|------------------|-------------------|----------------|-------------------------------|
| 冒泡   | 稳定   | $$O(n^2)$$       | $$O(n^2)$$        | $$O(1)$$       | n小时较好                     |
| 选择   | 不稳定 | $$O(n^2)$$       | $$O(n^2)$$        | $$O(1)$$       | n小时较好                     |
| 插入   | 稳定   | $$O(n^2)$$       | $$O(n^2)$$        | $$O(1)$$       | 大部分已排序时较好            |
| 堆排   | 不稳定 | $$O(n log n)$$   | $$O(n log n)$$    | $$O(1)$$       | n大时较好                     |
| 归并   | 稳定   | $$O(n log n)$$   | $$O(n log n)$$    | $$O(1)$$       | n大时较好                     |
| 快速   | 不稳定 | $$O(n log n)$$   | $$O(n2)$$         | $$O(n log n)$$ | n大时较好                     |
| 希尔   | 不稳定 | $$O(n log^2 n)$$ | $$O(n^s)$$, 1<s<2 | $$O(1)$$       | s是所选分组                   |
| 基数   | 稳定   | $$O(log _R B)$$  | $$O(log _R B)$$   | $$O(n)$$       | B是真数(0-9)，R是基数(个十百) |

## 简单实现

C++实现：
```cpp
{% include_relative code/xxx_sort.hpp %}
```
```cpp
{% include_relative code/xxx_sort_test.cpp %}
```

## 延伸问题及解答

排序算法可以延伸解决其他问题，以下是几个例子：

**问题1** 给定序列，Random shuffle 随机化序列（洗牌算法）  
   **思路**：类似与选择排序。随机选择第1到第i之间的数与第i交换，可以用一句伪代码表达 `for i:=1 to n do swap(a[i], a[random(1,i)]);`  
   **证明**：见[这里](../../../2014/12/11/prove-random-shuffle.html)  

**问题2** 给定序列，求序列的逆序数  
   **思路**：可以用类似 冒泡排序 或 归并排序 解决来求解。冒泡排序的思路，计数第i个数向右侧冒泡的次数，累计冒泡总数。归并排序的思路，每次归并两个已排序序列发现右侧逆序数可以根据左侧序列所剩长度求和求得，具体逻辑见代码。归并排序的思路有更好的时间效率  
   **证明**：略  

分别给出Python代码解答如下：  
````python
{% include_relative code/sorting_extention.py %}
````

输出结果：
````markdown
The array after random shuffle:  [8, 1, 9, 4, 5, 3, 0, 7, 6, 2]
The inversions number of array  [3, 8, 6, 7, 9, 2, 1, 5, 0, 4] :  30
The inversions number of array  [3, 8, 6, 7, 9, 2, 1, 5, 0, 4] :  30
````
