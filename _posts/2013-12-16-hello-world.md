---
typora-root-url: ../
title: "Hello World"
categories: "technology"
tags:
  - markdown
---

这是测试页面，测试显示的效果，用Markdown写博文，和一些实用的插件。内容主要介绍用Hexo建博客，同时以下是简介及实例作为笔记备忘。


## 用Jekyll/Hexo在Github上建博客

英文 [Jekyll • Simple, blog-aware, static sites](http://jekyllrb.com/)  中文 [Jekyll 简单静态博客网站生成器](http://jekyllcn.com/)  
[Hexo官方文档](https://hexo.io/zh-cn/docs/)

---

## Markdown 语法简介

现在用Markdown写博文很流行也确实很方便，很多网站的评论也开始支持Markdown语言。这种轻度标记语言挺简单，并且可以很轻松写出一些排版清楚的文字。  
[Markdown 语法简介](http://wowubuntu.com/markdown/ )  
[讲解 Markdown](http://alfred-sun.github.io/blog/2015/01/10/markdown-syntax-documentation/)  

### 语法文档

![markdownsheet](/images/markdownsheet.png )

### 长标题测试测试测试测试测试测试测试测试测试测试测试测试

### 列表

无序号列表：

* kram
+ down
- now

嵌套的列表：

Create nested lists by indenting list items by two spaces.

1. Item 1
  1. A corollary to the above item.
  2. Yet another point to consider.
2. Item 2
  -  A corollary that does not need to be ordered.
  -  This is indented four spaces, because it's two spaces further than the item above.
  -  You might want to consider making a new list.
3. Item 3

### 引用

Markdown 标记区块引用是使用类似 email 中用 `>` 的引用方式：

> This is the first level of quoting.
>
> > This is nested blockquote.
>
> Back to the first level.

### 表格

建表格使用连字符 `` - `` 和竖线 `` | `` ，区分开表头和单元格：

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

想好看一些的话，也可以在开头和结尾加竖线：

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

顶部的连字符无需一定匹配表头文本的长度（但必须保证至少3个连字符）；也可以添加行内的Markdown语法文本，如链接、加粗、删除线等：

| Name          | Description                  |
| ------------- | ---------------------------- |
| Help          | ~~Display the~~ help window. |
| Close         | _Closes_ a window            |

表头行使用冒号:实现表格内列的文本对齐方式：

| Left-Aligned  | Center Aligned    | Right Aligned |
| :------------ | :---------------: | ------------: |
| col 3 is      | some wordy text   | $1600         |
| col 2 is      | centered          | $12           |
| zebra stripes | are neat          | $1            |
| col 3 is      | some wordy text   | $1600         |
| col 2 is      | centered          | $12           |
| zebra stripes | are neat          | $1            |

冒号在最左边表示该列文本左对齐，最右边表示文本右对齐，两边都加冒号表示居中对齐文本。

---

## 插件演示

写文章/代码用到的第三方插件的使用方法，主要是代码高亮、数学公式美化的功能。

### CSS额外定义

**按钮的效果：**

**示例：**

`<kbd>M-x package-list-packages</kbd> , then <kbd>U</kbd> followed by <kbd>x</kbd>.`

**效果：**

<kbd>M-x package-list-packages</kbd> , then <kbd>U</kbd> followed by <kbd>x</kbd>.

### 代码高亮

**示例：**

````markdown
​```cpp
class Voila {
public:
    // Voila
    static const string VOILA = "Voila";
    // will not interfere with embedded tags.
}
​```
````

```cpp
class Voila {
public:
    // Voila
    static const string VOILA = "Voila";
    // will not interfere with embedded tags.
}
```

### LATEX显示数学公式 MathJax

**示例：**

```markdown
Simple inline $a = b + c$.

$$(a_1,b_1,a_2,b_2,\cdots,an,bn)$$

$$(O(1))$$

$$(a1,a2,\cdots,a_n,b_1,\cdots,b_n)$$

$$a^2 + b^2 = c^2$$

数学公式 $$(a1,a2,\cdots,a_n,b_1,\cdots,b_n)$$ 和文字

$$\frac{\partial u}{\partial t}
= h^2 \left( \frac{\partial^2 u}{\partial x^2} +
\frac{\partial^2 u}{\partial y^2} +
\frac{\partial^2 u}{\partial z^2}\right)$$

$$
\left[
    \begin{array}{cc|c}
      1&2&3\newline
      4&5&6
    \end{array}
\right] 
$$
```

Simple inline $a = b + c$.

$$(a_1,b_1,a_2,b_2,\cdots,an,bn)$$

$$(O(1))$$

$$(a1,a2,\cdots,a_n,b_1,\cdots,b_n)$$

$$a^2 + b^2 = c^2$$

数学公式 $(a1,a2,\cdots,a_n,b_1,\cdots,b_n)$ 和文字

$$\frac{\partial u}{\partial t}
= h^2 \left( \frac{\partial^2 u}{\partial x^2} +
\frac{\partial^2 u}{\partial y^2} +
\frac{\partial^2 u}{\partial z^2}\right)$$

$$
\left[
    \begin{array}{cc|c}
      1&2&3\newline
      4&5&6
    \end{array}
\right] 
$$


### Flowchart / Mermaid 流程图

目前使用 [flowchart.js](https://github.com/adrai/flowchart.js)
[flowchart docs](http://flowchart.js.org/)
[mermaid docs](http://knsv.github.io/mermaid/index.html#mermaid)

**示例：**

```markdown
st=>start: Start|past:>http://www.google.com[blank]
e=>end: End:>http://www.google.com
op1=>operation: My Operation|past
op2=>operation: Stuff|current
sub1=>subroutine: My Subroutine|invalid
cond=>condition: Yes
or No?|approved:>http://www.google.com
c2=>condition: Good idea|rejected
io=>inputoutput: catch something...|request

st->op1(right)->cond
cond(yes, right)->c2
cond(no)->sub1(left)->op1
c2(yes)->io->e
c2(no)->op2->e
```

```flow
st=>start: Start|past:>http://www.google.com[blank]
e=>end: End:>http://www.google.com
op1=>operation: My Operation|past
op2=>operation: Stuff|current
sub1=>subroutine: My Subroutine|invalid
cond=>condition: Yes
or No?|approved:>http://www.google.com
c2=>condition: Good idea|rejected
io=>inputoutput: catch something...|request

st->op1(right)->cond
cond(yes, right)->c2
cond(no)->sub1(left)->op1
c2(yes)->io->e
c2(no)->op2->e
```

## 结束语

**最后，保持现在这种激情写博文！**
