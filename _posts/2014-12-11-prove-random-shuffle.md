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

参考VS2008中`<algorithm>`文件中`_Random_shuffle`代码：

```cpp
template<class _RanIt,
    class _Diff> inline
    void _Random_shuffle(_RanIt _First, _RanIt _Last, _Diff *)
    {    // shuffle [_First, _Last)
    _DEBUG_RANGE(_First, _Last);
    const int _RANDOM_BITS = 15;    // minimum random bits from rand()
    const int _RANDOM_MAX = (1U << _RANDOM_BITS) - 1;

    _RanIt _Next = _First;
    for (unsigned long _Index = 2; ++_Next != _Last; ++_Index)
        {    // assume unsigned long big enough for _Diff count
        unsigned long _Rm = _RANDOM_MAX;
        unsigned long _Rn = ::rand() & _RANDOM_MAX;
        for (; _Rm < _Index && _Rm != ~0UL;
            _Rm = _Rm << _RANDOM_BITS | _RANDOM_MAX)
            _Rn = _Rn << _RANDOM_BITS
                | (::rand() & _RANDOM_MAX);    // build random value

        std::iter_swap(_Next, _First + _Diff(_Rn % _Index));    // swap a pair
        }
    }
```

`std::iter_swap(_Next, _First + _Diff(_Rn % _Index));` 中 `_Rn % _Index` 是产生 `0 ~ _Index-1`中的一个随机数。
可以用一句伪代码表达 `for i:=0 to n-1 do swap(a[i], a[random(0,i)]);`。为了证明方便，将伪代码表述为 `for i:=1 to n do swap(a[i], a[random(0,i)]);`。

## 问题的数学表述

某个序列 `a[:]` 经过  `for i:=1 to n do swap(a[i], a[random(0,i)]);` 操作后得到新的序列 `a[:]`，求证，第 i 个元素为 x (x 为原序列任意元素) 的概率 $p_{(i=x)}=\frac{1}{n}$

## 证明

采用数学归纳法证明

1. 当 $n = 2$ 时，显然成立，即 `for i:=1 to 2 do swap(a[i], a[random(1,i)]);` 操作，可以得出 $p_{(i = x)} = \frac{1}{2}$，对于 $i$ 在 $[1, 2]$ 内, $x$是序列 $a$ 的某一元素 成立
2. **假设** $n = k, (k >= 2)$ 成立，即 `for i:=1 to k do swap(a[i], a[random(1,i)]);` 操作，可以得出 $p_{(i = x)} = \frac{1}{k}$，对于 $i$ 在 $[1, k]$ 内, $x$是序列 $a$ 的某一元素 成立；
   **则** $n = k + 1$ 时，操作 `for i:=1 to k+1 do swap(a[i], a[random(1,i)]);`
   可分解为 `for i:=1 to k do swap(a[i], a[random(1, i)]); swap(a[k+1], a[random(1, k+1)]);` 两步操作，

    * 第一句伪代码执行得出：前 k 次循环所得序列各个元素出现概率为 $$p^{(k)}_{(i = x)}$$ 其中 $$p^{(k)}_{(i = x)} = \frac{1}{k}$$，对于 $i$ 在 $[1, k]$ 内, $x$是序列 $a$ 的某一元素，
    * 第二句伪代码执行得出：经过第 k+1 次循环所得序列各个元素出现概率为 $p^{(k+1)}_{(i = x)}$

      * 其中 对于 $i$ 在 $[1, k]$ 内, $$p^{(k+1)}_{(i = x)} = p^{(k)}_{(i = x)} * \frac{k}{k+1} = \frac{1}{k} * \frac{k}{k+1} = \frac{1}{k+1}$$;
      * 元素 $x$ 在 $[1, k]$ 中某个位置 （无论是在 $i$ 位置或不是 $i$ 位置），只要交换 $x$ 所在的位置和 $k+1$ 位置即可，故，$$p^{(k+1)}_{(i = x)} = \frac{1}{k+1}$$，对于$i = k+1$;

      所以， $$p^{(k+1)}_{(i = x)} = \frac{1}{k+1}$$ ，即，对于 $n = k + 1$, $$p_{(i = x)} = \frac{1}{k+1}$$

综上，由1，2得 $p_{(i = x)} = \frac{1}{n}$ 成立，问题得到证

