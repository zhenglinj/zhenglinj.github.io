---
layout: post
title: "Emacs 开箱即用 —— 简易说明书"
excerpt: "Emacs 常用操作的一些笔记，以及在使用 Emacs 过程遇上的问题会不断更新在这里。"
category: "technology"
tags: [emacs, notes]
---
{% include JB/setup %}

本文主要介绍Emacs基本操作及某些插件操作，不会介绍Emacs如何配置。同时，记录使用Emacs过程遇上的问题。

---

## 前言

**EMACS 的缩写**

EMACS = Editor MACroS (Offical) 宏编辑器
还有非官方缩写：

- EMACS = Esc + Meta + Alt + Ctrl + Shift
- EMACS = Emacs Make All Computer Smarter/Slow
- ......

简介：[Emacs - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/Emacs)

**符号约定**

本文中所出现的符号： <kbd>C</kbd> 代表 <kbd>Ctrl</kbd>，<kbd>M</kbd> 代表 <kbd>Alt</kbd> 。示例： <kbd>C-h 其他键</kbd> => <kbd>Ctrl+h 其他键</kbd>； <kbd>M-x 命令</kbd> => <kbd>Alt+x 命令</kbd>。
其中 <kbd>C-h</kbd>, <kbd>C-x</kbd>, <kbd>C-c</kbd>, <kbd>C-u</kbd> 一般作为前缀操作 (Prefix Command)，前缀操作要加上其他快捷键组合完成功能。如： <kbd>C-h t</kbd> => Emacs Tutorail

官方资料 [GNU Emacs Manual](http://www.gnu.org/software/emacs/manual/html_node/emacs/index.html#Top )

---

### 基本概念

- buffer: 
- major mode: 
- minor mode: 

## 帮助文档

Emacs 的帮助文档很强大

+ `F1 其他键` 或 `C-h 其他键`，`C-h h` 查看所有其他键选项；
+ `M-x info` 可以查看各个插件的内置帮助文档；

内置帮助文档 Tutorial 介绍到基本操作还是不错的。`C-h t` 则默认英文显示 Tutorial，或者 `C-u C-h t` 输入指定语言及编码的 Tutorial。

<!-- TODO -->
基本操作见相关资料：[Mastering Emacs](https://www.masteringemacs.org/)

---

## 常用的Major Mode

`C-h m` 可以查看当前 buffer 的 Major Mode, Minor Mode 等信息，并且可以看 Major Mode 的相关快捷键。

### Info Mode

Info Mode 查看某些插件的内置帮助文档。`M-x info` 可以看到有介绍很多 Mode / 插件 的帮助文档，基本操作可以 `C-h m` 查看。

### Ediff Mode

Ediff Mode 可以对比多个文件。`M-x ediff` 或 `M-x ediff3`，再根据提示输入指定2/3个要对比的文件，采用A/B模式对比2/3个文件。在该模式下输入 `h` 可以看到具体操作。
官方文档：[Ediff User's Manual](http://www.chemie.fu-berlin.de/chemnet/use/info/ediff/ediff.html )

### Org Mode

Org Mode 可以编辑 `*.org` 文件, org 文件可以转换成 `HTML`, `Markdown`, `LATEX`, `ODT` 等等，所以可以用来写博客，写作，写计划TODO等等。
官方网站（含文档）：[Org mode for Emacs](http://orgmode.org/)

---

## 开发常用Minor Mode

### Magit

**依赖**：git
Magit Mode 可以在 Emacs 中操作 git 完成版本工具的基本操作，具体帮助见如下链接。
官方介绍：[Magit! A Git Porcelain inside Emacs](http://magit.vc/)
快捷键：[Magit Cheatsheet](http://daemianmack.com/magit-cheatsheet.html)

### Diff-hl

**依赖**：git, svn, hg, ... 等版本管理工具
在侧边 `fringe` 高亮显示 增，删，改 的行

### GGtag Mode (Global)

**依赖**：global
GGtag Mode C/C++/Java等源代码自动跳转功能。`M-x ggtags-create-tags` 生产 *TAG 文件，`M-.` 跳转到定义或引用处，`M-,` 跳转回来

### Flycheck Mode

**依赖**：不同语言依赖不同语法检查工具，如：gcc/clang, g++/clang++, python-flake8, gofmt, ...
动态语法检查

### Auto-complete Mode

**依赖**：不同语言依赖不同代码补全后端工具，如：clang, python-jedi, gocode, ...
代码自动补全

---

## 日常工作Minor Mode

### Evernote (Geeknote)

在 Emacs 中编辑 印象笔记

### SDCV / YDCV

SDCV (Star Dictionary Console Version) 和 [YDCV (You Dao Console Version)](https://github.com/zhenglinj/ydcv-el) 可以在 Emacs 中查字典

- SDCV 可以搜索本地 StarDict 字典。`C-c ; t` 查找光标所在单词，并气泡提示显示结果；`C-c ; b` 查找光标所在单词或输入，并在buffer中显示结果；
- [YDCV](https://github.com/zhenglinj/ydcv-el) 可以搜索本地 StarDict 字典，也会搜索有道翻译。`C-c ; t` 查找光标所在单词，并气泡提示显示结果；`C-c ; b` 查找光标所在单词或输入，并在buffer中显示结果；
