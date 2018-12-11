---
layout: post
title: "一个数学题..."
description: ""
draft: true
category: "life"
tags: [mathematic, life]
---
{% include JB/setup %}

## 问题

今天请你解个微分方程，结果有惊喜哦(公式呈现有点慢，请耐心等待)。
方程如下：

$$a p^2 (o u - 1) H'(ap^2y) + (o u - 1) D_a = (a p^2)^2 y H''(ap^2y)$$

已知： $$H(0) = Birth$$，$$H'(ap^2) = \frac{2o u - D_a}{ap^2}$$ （式中 $$Birth$$ 为常数，上式中 $$a,p,o,u,D_a$$ 都是常数）

求解： $$H(a p^2 y)$$

<p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p>

## 木有答案……
<p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p>

**以下是解：**

$$a p^2 (o u - 1) H'(a p^2 y) + (o u - 1) D_a = (a p^2)^2 y H''(a p^2 y)$$

整理得：

$$(o u - 1) [ a p^2 H'(a p^2 y) + D_a ] = (a p^2)^2 y H''(a p^2 y)$$

可以把 $$H(a p^2 y)$$ 看成整体，记为 $$H$$；一阶导为 $$\frac{dH}{dx} = a p^2 H'(a p^2 y)$$，二阶导为$$\frac{d^2H}{dy^2} = (a p^2)^2 H''(a p^2 y)$$

重新写式子得：

$$(o u - 1) [\frac{dH}{dy}  + D_a ] = y \frac{d^2H}{dy^2}$$

记 $$h(y) = \frac{dH}{dy}$$

$$(o u - 1) [ h(y)  + D_a ] = y \frac{dh}{dy}$$

分离变量：

$$\frac{1}{h+D_a} dh = \frac{o u - 1}{y} dy$$

两边分别积分：

$$\ln{(h(y) + D_a)} = (o u - 1)\ln{y} + C_1$$

求得：

$$h(y) + D_a = C_2 y^{o u - 1}$$

已知： $$h(1) = ap^2H'(ap^2) = 2o u - D_a$$ ， 故 $$C_2 = 2o u$$

$$\frac{dH}{dy} = - D_a + 2o u y^{o u-1}$$

两边对$$y$$求积分，即：

$$H(ap^2y) = -D_a y + 2y^{o u} + C_3$$

已知：  $$H(0) = Birth$$ ， 故 $$C_3 = Birth$$

<p></p>

**得出结论：**

$$H(ap^2y) = Birth - D_ay + 2y^{o u}$$

**即：祝你生日快乐** $$Happy \ Birth-Day \ To \ You$$

其实看到 $$H(0) = Birth$$，再结合女主角你的一点个人信息，大概也就能猜出来可能的样式。

<p></p>

## 综上

**初衷：**了解你喜欢数学，就想用一种特别的方式祝你生日快乐

**过程：**兢兢战战地在学霸兼考神面前码下数学公式

**目的：**希望你看到会有些惊喜，也能感受到我真诚用心！

**欠缺：**码完这段文字又有点后悔，题目本身的繁琐超过出题的目的，时间水平有限（本该搞成线性方程组的）；页面排版有点凌乱，毕竟是业余的

**最后：**时间仓促，错误难免，欢迎指正

<p></p>

---
