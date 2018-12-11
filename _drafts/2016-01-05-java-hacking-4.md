---
layout: post
title: "Java 之禅 扩展"
description: "Java 学习笔记之扩展篇"
category: "technology"
draft: false
analytics: true
comments: true
tags: [java, 笔记]
---
{% include JB/setup %}

Java 学习笔记之扩展篇

---

4.1. 相关知识

4.1.1. 云计算，分布式，高可用，可扩展

4.1.2. 虚拟化

https://linuxcontainers.org/

http://www.linux-kvm.org/page/Main_Page

http://www.xenproject.org/

https://www.docker.io/

4.1.3. 监控

http://www.nagios.org/

http://ganglia.info/

4.1.4. 负载均衡

http://www.linuxvirtualserver.org/

4.1.5. 学习使用git

https://github.com/

https://git.oschina.net/

4.1.6. 学习使用maven

http://maven.apache.org/

4.1.7. 学习使用gradle

http://www.gradle.org/

4.1.8. 学习一个小语种语言

Groovy Scala LISP, Common LISP, Schema, Clojure R Julia Lua Ruby

4.1.9. 尝试了解编码的本质

了解以下概念 ASCII, ISO-8859-1 GB2312, GBK, GB18030 Unicode, UTF-8 不使用 String.getBytes() 等其他工具类/函数完成下面功能

public static void main(String[] args) throws IOException {
    String str = "Hello, 我们是中国人。";
    byte[] utf8Bytes = toUTF8Bytes(str);
    FileOutputStream fos = new FileOutputStream("f.txt");
    fos.write(utf8Bytes);
    fos.close();
}
public static byte[] toUTF8Bytes(String str) {
    return null; // TODO
}
想一下上面的程序能不能写一个转GBK的？ 写个程序自动判断一个文件是哪种编码

4.1.10. 尝试了解时间的本质

时区 & 冬令时、夏令时 http://en.wikipedia.org/wiki/Time_zone ftp://ftp.iana.org/tz/data/asia http://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9C%8B%E6%99%82%E5%8D%80

闰年 http://en.wikipedia.org/wiki/Leap_year

闰秒 ftp://ftp.iana.org/tz/data/leapseconds

System.currentTimeMillis() 返回的时间是什么

4.1.11. 参考资料

http://git-scm.com/

http://en.wikipedia.org/wiki/UTF-8

http://www.iana.org/time-zones

4.2. 扩展学习

4.2.1. JavaScript知识

4.2.1.1. 什么是prototype

修改代码，使程序输出“1 3 5”： http://jsfiddle.net/Ts7Fk/

4.2.1.2. 什么是闭包

看一下这段代码，并解释一下为什么按Button1时没有alert出“This is button: 1”，如何修改： http://jsfiddle.net/FDPj3/1/

4.2.1.3. 了解并学习一个JS框架

jQuery ExtJS ArgularJS

4.2.1.4. 写一个Greasemonkey插件

http://en.wikipedia.org/wiki/Greasemonkey
4.2.1.5. 学习node.js

http://nodejs.org/

4.2.2. 学习html5

ArgularJS，https://docs.angularjs.org/api

4.2.3. 参考资料

http://www.ecmascript.org/

http://jsfiddle.net/

http://jsbin.com/

http://runjs.cn/

http://userscripts.org/

五、 推荐书籍

《深入Java虚拟机》

《深入理解Java虚拟机》

《Effective Java》

《七周七语言》

《七周七数据》

《Hadoop技术内幕》

《Hbase In Action》

《Mahout In Action》

《这就是搜索引擎》

《Solr In Action》

《深入分析Java Web技术内幕》

《大型网站技术架构》

《高性能MySQL》

《算法导论》

《计算机程序设计艺术》

《代码大全》

《JavaScript权威指南》
