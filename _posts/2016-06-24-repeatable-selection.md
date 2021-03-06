---
typora-root-url: ../
title: "“可重复遍历有序选择”问题"
categories: "mathematic"
tags:
  - mathematic
---
遇到排列组合中的一类问题，上网搜索了下还没有这类问题的解答，所以思考该问题同时顺便写下这篇文章记录下。抽象地用数学语言描述，K 个不同元素可重复地有序地选择 N 次（其中 N >= K），且 K 个元素全出现，问有多少种可能。

---

## 问题描述

同事问了一个排列组合问题，思考了许久并且上网搜索了下没有这类问题。问题如下：一班级有K位同学，每次随机抽一位同学拍照，拍完后该同学回到班级中，重复以上拍照N次。问K位同学都拍照的概率。

抽象以上问题，K 个不同元素标记为  ，可重复有序选择 N 次，其中 ，且 K 个元素全出现，该情况总数。暂时称这类问题为“可重复遍历有序选择”。

不考虑所有同学都出现，N次拍照过程是“可重复有序选择”的过程。考虑到所有同学都出现，N次拍照过程是“可重复遍历有序选择”的过程。所以概率为：“可重复遍历有序选择” / “可重复有序选择”

## 问题解答

首先，考虑“可重复有序选择”简单问题，K 个不同元素，可重复有序选择 N 次，显然选择总数为 $$K^N$$

再，考虑“可重复遍历有序选择”，假设这样 k 个元素 n $$(n >= k)$$ 次“可重复遍历有序选择”总数为 $$a(n, k)$$，稍微计算。

当 $$k = 1$$ 时，即可选择的元素为 $${ 1 }$$，$$a(1, 1) = 1, a(2, 1) = 1, a(3, 1) = 1$$；

当 $$k = 2$$ 时，即可选择的元素为 $${ 1, 2 }$$，$$a(2, 2)$$ 情况则有：$$(1, 2), (2, 1)$$，$$a(3, 2)$$ 情况则有：$$(1, 1, 2), (1, 2, 1), (1, 2, 2), (2, 1, 1), (2, 1, 2), (2, 2, 1)$$；

得以下公式：

$$ a(1, 1) = 1$$,

$$a(2, 1) = 1$$, $$a(2, 2) = 2$$,

$$a(3, 1) = 1$$, $$a(3, 2) = 6$$, $$a(3, 3) = 6$$,

$...$

**思路**：尝试将“可重复遍历有序选择”转化为“可重复有序选择”。

则可以将这个问题转化为：k 个元素先选择出 i 个元素 $$(i = 1, 2, ..., k)$$，再在对 i 个元素“可重复遍历有序选择”得 $$a(n, i)$$，$$a(n,i)$$对 $$i, (i = 1, 2, ..., k)$$ 求和等于“可重复有序选择”总数，即，

$$\sum\limits_{i=1}^k C_k^i a(n, i) = k^n, k = 1, 2, ..., n$$

从集合角度简单证明：等式右边能覆盖所有可能性，并且求和中的各个求和项彼此没有交集；等式左边可以分解成右边的子问题；两个结果集合一一映射。从而证明等式成立

对 $$n = 3$$ 举例验证发现有以下线性方程组：

$$C_1^1 a(3, 1) = 1^3$$,

$$C_2^1 a(3, 1) + C_2^2 a(3, 2) = 2^3$$,

$$C_3^1 a(3, 1) + C_3^2 a(3, 2) + C_3^3 a(3, 3) = 3^3$$,

矩阵表示一般情况下该线性方程组：

$$
\begin{equation*}
\left[
\begin{matrix}
 1           & 0          & 0          & 0          & \cdots     & 0          & 0      \\
 2           & 1          & 0          & 0          & \cdots     & 0          & 0      \\
 3           & 3          & 1          & 0          & \cdots     & 0          & 0      \\
 4           & 6          & 4          & 1          & \cdots     & 0          & 0      \\
 \vdots      & \vdots     & \vdots     & \vdots     & \ddots     & \vdots     & \vdots \\
 C_{n-1}^1   & C_{n-1}^2  & C_{n-1}^3  & C_{n-1}^4  & \cdots     & 0          & 0      \\
 C_{n}^1     & C_{n}^2    & C_{n}^3    & C_{n}^4    & \cdots     & 0          & 0      \\
\end{matrix}
\right]

*

\left[
\begin{matrix}
 a(n, 1)     \\
 a(n, 2)     \\
 a(n, 3)     \\
 a(n, 4)     \\
 \vdots      \\
 a(n, n-1)   \\
 a(n, n)     \\
\end{matrix}
\right]

=

\left[
\begin{matrix}
 1^n         \\
 2^n         \\
 3^n         \\
 4^n         \\
 \vdots      \\
 (n-1)^n         \\
 (n)^n         \\
\end{matrix}
\right]

\end{equation*} \tag{1}
$$

暂时没找到解析解答，用数值方法解该方程组的数值解。n 较大时因为数值计算误差会有问题，以下对 n = 10 计算，并数值方法验证：

```python
import numpy as np

NUM = 8


def A(n, k):
    if k > n:
        raise ValueError('n >= k')
    ret = 1
    for i in range(n, n - k, -1):
        ret *= i
    return ret


def C(n, k):
    if k > n:
        raise ValueError('n >= k')
    if k > n / 2:
        return C(n, n - k)
    else:
        return int(A(n, k) / A(k, k))


def algebra_result(n=NUM):
    params_mat = np.matrix(
        [
            [C(k, i) if k >= i else 0 for i in range(1, n + 1)]
            for k in range(1, n + 1)
        ])
    belta_mat = np.matrix([i ** n for i in range(1, n + 1)]).getT()
    result = params_mat.getI() * belta_mat
    return result


def numerical_result(n=NUM):
    def _fill_nums(n, k, x=[]):
        for i in range(1, k + 1):
            x.append(i)
            if n == 1:
                yield x
            else:
                for list in _fill_nums(n - 1, k, x):
                    yield list
            x.pop()

    result = [0] * n
    for k in range(1, n + 1):
        for x in _fill_nums(n, k):
            if len(set(x)) == k:
                result[len(set(x)) - 1] += 1
    return result


def main(args=None):
    print("K items repeatable all selection N times (N >= k, N = {0:d}):".format(NUM))
    k = 1
    result = algebra_result()
    print("Algebra result:")
    for r in result:
        print("a({0:d}, {1:d}) = {2:d} ({3:f}),".format(NUM, k, int(np.round(r)), np.float(r)))
        k += 1
    print()
    k = 1
    result = numerical_result()
    print("Numerical result:")
    for r in result:
        print("a({0:d}, {1:d}) = {2:d},".format(NUM, k, r))
        k += 1


main()
```

结果如下：

```
K items repeatable all selection N times (N >= k, N = 8):
Algebra result:
a(8, 1) = 1 (1.000000),
a(8, 2) = 254 (254.000000),
a(8, 3) = 5796 (5796.000000),
a(8, 4) = 40824 (40824.000000),
a(8, 5) = 126000 (126000.000000),
a(8, 6) = 191520 (191520.000000),
a(8, 7) = 141120 (141120.000000),
a(8, 8) = 40320 (40320.000000),

Numerical result:
a(8, 1) = 1,
a(8, 2) = 254,
a(8, 3) = 5796,
a(8, 4) = 40824,
a(8, 5) = 126000,
a(8, 6) = 191520,
a(8, 7) = 141120,
a(8, 8) = 40320,
```

