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

## 复杂度比较

[zh.Wikipedia](https://zh.wikipedia.org/wiki/%E6%8E%92%E5%BA%8F%E7%AE%97%E6%B3%95)  
[en.Wikipedia](https://en.wikipedia.org/wiki/Sorting_algorithm)  

| 排序法                                                       | 稳定度 | 平均时间       | 最差情形       | 额外空间       | 备注                                                 |
| ------------------------------------------------------------ | ------ | -------------- | -------------- | -------------- | ---------------------------------------------------- |
| [冒泡排序](https://zh.wikipedia.org/wiki/%E6%B0%A3%E6%B3%A1%E6%8E%92%E5%BA%8F) | 稳定   | $$O(n^2)$$     | $$O(n^2)$$     | $$O(1)$$       | n小时较好                                            |
| [选择排序](https://zh.wikipedia.org/wiki/%E9%80%89%E6%8B%A9%E6%8E%92%E5%BA%8F) | 不稳定 | $$O(n^2)$$     | $$O(n^2)$$     | $$O(1)$$       | n小时较好                                            |
| [插入排序](https://zh.wikipedia.org/wiki/%E6%8F%92%E5%85%A5%E6%8E%92%E5%BA%8F) | 稳定   | $$O(n^2)$$     | $$O(n^2)$$     | $$O(1)$$       | 大部分已排序时较好                                   |
| [堆排序](https://zh.wikipedia.org/wiki/%E5%A0%86%E6%8E%92%E5%BA%8F) | 不稳定 | $$O(n log n)$$ | $$O(n log n)$$ | $$O(1)$$       | n大时较好                                            |
| [归并排序](https://zh.wikipedia.org/wiki/%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8F) | 稳定   | $$O(n log n)$$ | $$O(n log n)$$ | $$O(n)$$       | n大时较好                                            |
| [快速排序](https://zh.wikipedia.org/wiki/%E5%BF%AB%E9%80%9F%E6%8E%92%E5%BA%8F) | 不稳定 | $$O(n log n)$$ | $$O(n^2)$$     | $$O(n log n)$$ | n大时较好                                            |
| [桶排序](https://zh.wikipedia.org/wiki/%E6%A1%B6%E6%8E%92%E5%BA%8F) | 稳定   | $$O(n)$$       | $$O(n)$$       | $$O(m)$$       | 将值为i的元素放入i号桶，最后依次把桶里的元素倒出来。 |

## 简单实现

C++实现排序算法：
```cpp
// ************************  xxx_sort.hpp  ***************************
//                  Generic sorting algorithms
//                overloading of < and = required

#include <cstdlib>

// conflict with <algorithms>, <queue>
template<class T>
inline void swap(T& e1, T& e2) {
    T tmp = e1; e1 = e2; e2 = tmp;
}

template<class T>
void insertion_sort(T data[], size_t n) {
    for (size_t i = 1, j; i < n; i++) {
        T tmp = data[i];
        for (j = i; j > 0 && tmp < data[j-1]; j--)
            data[j] = data[j-1];
        data[j] = tmp;
    }
}

template<class T>
void selection_sort(T data[], size_t n) {
    for (size_t i = 0, least, j; i < n-1; i++) {
        for (j = i+1, least = i; j < n; j++)
            if (data[j] < data[least])
                least = j;
        swap(data[least], data[i]);
    }
}

template<class T>
void bubble_sort(T data[], int n) {
    for (int i = 0; i < n-1; i++)
        for (int j = n-1; j > i; --j)
            if (data[j] < data[j-1])
                swap(data[j], data[j-1]);
}

template<class T>
void shell_sort(T data[], size_t size) {
    register int i, j, h_cnt, h;
    int increments[20], k;
    //  create an appropriate number of increments h
    for (h = 1, i = 0; h < size; i++) {
        increments[i] = h;
        h = 3*h + 1;
    }
    // loop on the number of different increments h
    for (i--; i >= 0; i--) {
        h = increments[i];
        // loop on the number of subarrays h-sorted in ith pass
        for (h_cnt = h; h_cnt < 2*h; h_cnt++) {
            // insertion sort for subarray containing every hth element of array data
            for (j = h_cnt; j < size; ) {
                T tmp = data[j];
                k = j;
                while (k-h >= 0 && tmp < data[k-h]) {
                    data[k] = data[k-h];
                    k -= h;
                }
                data[k] = tmp;
                j += h;
            }
        }
    }
}

template<class T>
void _move_down(T data[], int first, int last) {
    int largest = 2*first + 1;
    while (largest <= last) {
        if (largest < last && // first has two children (at 2*first+1 and
            data[largest] < data[largest+1]) // 2*first+2) and the second
            largest++;                      // is larger than the first;

        if (data[first] < data[largest]) {   // if necessary,
            swap(data[first], data[largest]);// swap child and parent,
            first = largest;                // and move down;
            largest = 2*first+1;
        }
        else largest = last+1;  // to exit the loop: the heap property
    }                           // isn't violated by data[first];
}

template<class T>
void heap_sort(T data[], int size) {
    int i;
    for (i = size/2 - 1; i >= 0; --i)   // create the heap;
        _move_down(data, i, size-1);
    for (i = size-1; i >= 1; --i) {
        swap(data[0], data[i]); // move the largest item to data[i];
        _move_down(data, 0, i-1);  // restore the heap property;
    }
}

template<class T>
void _quick_sort(T data[], int first, int last) {
    int lower = first+1, upper = last;
    swap(data[first], data[(first+last)/2]);
    T bound = data[first];
    while (lower <= upper) {
        while (data[lower] < bound)
            lower++;
        while (bound < data[upper])
            upper--;
        if (lower < upper)
            swap(data[lower++], data[upper--]);
        else lower++;
    }
    swap(data[upper], data[first]);
    if (first < upper-1)
        _quick_sort (data,first,upper-1);
    if (upper+1 < last)
        _quick_sort (data,upper+1,last);
}

template<class T>
void quick_sort(T data[], int n) {
    int i, max;
    if (n < 2)
        return;
    for (i = 1, max = 0; i < n; i++)// find the largest
        if (data[max] < data[i])    // element and put it
            max = i;                // at the end of data[];
    swap(data[n-1], data[max]); // largest el is now in its
    _quick_sort(data, 0, n-2);     // final position;
}

template<class T>
void _merge_sort(T data[], int first, int last, T* temp) {
    if (first < last) {
        int mid = (first + last) / 2;
        _merge_sort(data, first, mid, temp);
        _merge_sort(data, mid+1, last, temp);

        // merge
        int i1 = 0, i2 = first, i3 = mid + 1;
        while (i2 <= mid && i3 <= last)
            if (data[i2] < data[i3])
                temp[i1++] = data[i2++];
            else
                temp[i1++] = data[i3++];
        while (i2 <= mid)
            temp[i1++] = data[i2++];
        while (i3 <= last)
            temp[i1++] = data[i3++];
        for (i1 = 0, i2 = first; i2 <= last; data[i2++] = temp[i1++]);
    }
}

template<class T>
void merge_sort(T data[], size_t size) {
    T* temp = new T[size];
    _merge_sort(data, 0, size-1, temp);
    delete[] temp;
}
```
C++测试用例：

```cpp
// ************************  xxx_sort.cpp  ***************************

#include <cstdlib>
#include <cstring>
#include <iostream>
#include <array>

#include "xxx_sort.hpp"

using namespace std;

int main(int argc, char *argv[])
{
  std::array<int, 8> arr = { 2, 45, 4, 7, 32, 63, 1, 3 };

  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    insertion_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    selection_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    shell_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    heap_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    quick_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    merge_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }

  return 0;
}
```

## 延伸问题及解答

排序算法可以延伸解决其他问题，以下是几个例子：

**问题1** 给定序列，Random shuffle 随机化序列（洗牌算法）  
   **思路**：类似与选择排序。随机选择第1到第i之间的数与第i交换，可以用一句伪代码表达 `for i:=1 to n do swap(a[i], a[random(1,i)]);`  
   **证明**：见[这里](../../../2014/12/11/prove-random-shuffle.html)  

```python
#!/usr/bin/env python3

import random


# 洗牌算法 Random shuffle
def random_shuffle(nums):
    for i in range(0, len(nums)):
        j = random.randint(0, i)
        if (i != j):
            nums[i], nums[j] = nums[j], nums[i]
    return


if __name__ == '__main__':
    nums = list(range(0, 10))
    random_shuffle(nums)
    print("The array after random shuffle: ", nums)
```

输出结果：

```markdown
The array after random shuffle:  [8, 1, 9, 4, 5, 3, 0, 7, 6, 2]
```



**问题2** 给定序列，求序列的逆序数  
   **思路**：可以用类似 冒泡排序 或 归并排序 解决来求解。冒泡排序的思路，计数第i个数向右侧冒泡的次数，累计冒泡总数。归并排序的思路，每次归并两个已排序序列发现右侧逆序数可以根据左侧序列所剩长度求和求得，具体逻辑见代码。归并排序的思路有更好的时间效率  
   **证明**：略  

````python
#!/usr/bin/env python3

import random


# 求序列的逆序数
# Merge sort
def inversions1(nums):
    counter = 0

    def merge_sort(nums):
        nonlocal counter
        if (len(nums) == 1):
            return
        mid = len(nums) // 2
        nums_l = nums[:mid]
        nums_r = nums[mid:]
        merge_sort(nums_l)
        merge_sort(nums_r)
        idx, lidx, ridx = 0, 0, 0
        while (lidx < len(nums_l) or ridx < len(nums_r)):
            if (lidx == len(nums_l)):
                nums[idx] = nums_r[ridx]
                ridx += 1
            elif (ridx == len(nums_r)):
                nums[idx] = nums_l[lidx]
                lidx += 1
            else:
                if (nums_l[lidx] <= nums_r[ridx]):
                    nums[idx] = nums_l[lidx]
                    lidx += 1
                else:
                    nums[idx] = nums_r[ridx]
                    ridx += 1
                    counter += len(nums_l) - lidx
            idx += 1
        return

    merge_sort(nums[:])
    return counter

# 求序列的逆序数
# Bubble sort
def inversions2(nums):
    counter = 0

    def bubble_sort(nums):
        nonlocal counter
        for i in range(len(nums), 1, -1):
            for j in range(1, i):
                if (nums[j-1] > nums[j]):
                    nums[j-1], nums[j] = nums[j], nums[j-1]
                    counter += 1
        return

    bubble_sort(nums[:])
    return counter


if __name__ == '__main__':
    nums = [3, 8, 6, 7, 9, 2, 1, 5, 0, 4]
    ret = inversions1(nums)
    print("The inversions number of array ", nums, ": ", ret)
    ret = inversions2(nums)
    print("The inversions number of array ", nums, ": ", ret)
````

输出结果：
````markdown
The inversions number of array  [3, 8, 6, 7, 9, 2, 1, 5, 0, 4] :  30
The inversions number of array  [3, 8, 6, 7, 9, 2, 1, 5, 0, 4] :  30
````
