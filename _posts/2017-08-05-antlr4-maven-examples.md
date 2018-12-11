---
typora-root-url: ../
title: "ANTLR v4 Examples (Java + Python)"
categories: "technology"
tags:
  - antlr4
---


<!-- TODO -->

---

## 背景介绍

由于项目中需要解析文本文件，将其解析转化成JSON格式。初步打算用类似编译器(Lex+Bison)前端工具生成解析器目标Java代码，经过一番搜索研究，这类工具可以称为："parser generators"。

经过阅读 Wikipedia [Comparison of parser generators](https://en.wikipedia.org/wiki/Comparison_of_parser_generators)，对上面所列出工具的一番对比，发现 ANTLR4 可以满足要求；再深入对该工具了解，发现 [ANTLR](http://www.antlr.org/index.html) 官网的介绍：

> ANTLR is a powerful parser generator that you can use to read, process, execute, or translate structured text or binary files. It’s widely used in academia and industry to build all sorts of languages, tools, and frameworks. Twitter search uses ANTLR for query parsing, with over 2 billion queries a day. The languages for Hive and Pig, the data warehouse and analysis systems for Hadoop, both use ANTLR. Lex Machina uses ANTLR for information extraction from legal texts. Oracle uses ANTLR within SQL Developer IDE and their migration tools. NetBeans IDE parses C++ with ANTLR. The HQL language in the Hibernate object-relational mapping framework is built with ANTLR.

既然经过诸多知名项目考验，那 ANTLR (ANother Tool for Language Recognition) 应该是值得学习的实用工具，本文给出该工具的使用例子，Java 目标语言 Maven 工程。


## 文档 & 代码示例

[ANTLR 4 Github 项目源码](https://github.com/antlr/antlr4)  
[ANTLR 4 Documentation](https://github.com/antlr/antlr4/blob/master/doc/index.md)  
[Offical Code Examples](https://media.pragprog.com/titles/tpantlr2/code/tpantlr2-code.tgz)  
[A copy of code in "The Definitive ANTLR 4 Reference" for ANTLR 4.6](https://github.com/blindpirate/the-definitive-antlr4-reference-code)  
[扩展巴科斯范式(EBNF)](https://zh.wikipedia.org/wiki/%E6%89%A9%E5%B1%95%E5%B7%B4%E7%A7%91%E6%96%AF%E8%8C%83%E5%BC%8F)  

## ANTLR4 -- Java Target Maven Example Project

[]()  

## ANTLR4 -- Python Target Example Project


## ANTLR4 testsuite

[](https://github.com/antlr/antlr4) `antlr4-tool-testsuite`

## ACE Editor with ANTLR4

ACE.js是流行的前端页面编辑器，由JavaScript实现。可以结合ANTLR4实现自定义的语言关键字高亮等基本功能。

[](https://github.com/antlr/antlr4/blob/master/doc/ace-javascript-target.md)  
