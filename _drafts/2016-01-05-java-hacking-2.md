---
layout: post
title: "Java 之禅 进阶"
description: "Java 学习笔记之进阶篇"
category: "technology"
draft: false
analytics: true
comments: true
tags: [java, 笔记]
---
{% include JB/setup %}

Java 学习笔记之进阶篇

---

2.1. Java底层知识

2.1.1. 学习了解字节码、class文件格式

http://en.wikipedia.org/wiki/Java_class_file

http://en.wikipedia.org/wiki/Java_bytecode

http://en.wikipedia.org/wiki/Java_bytecode_instruction_listings

http://www.csg.ci.i.u-tokyo.ac.jp/~chiba/javassist/

http://asm.ow2.org/

2.1.2. 写一个程序要求实现javap的功能（手工完成，不借助ASM等工具）

如Java源代码：

  public static void main(String[] args) {
    int i = 0;
    i += 1;
    i *= 1;
    System.out.println(i);
  }
编译后读取class文件输出以下代码：

public static void main(java.lang.String[]);
  Code:
   Stack=2, Locals=2, Args_size=1
   0:   iconst_0
   1:   istore_1
   2:   iinc    1, 1
   5:   iload_1
   6:   iconst_1
   7:   imul
   8:   istore_1
   9:   getstatic       #2; //Field java/lang/System.out:Ljava/io/PrintStream;
   12:  iload_1
   13:  invokevirtual   #3; //Method java/io/PrintStream.println:(I)V
   16:  return
  LineNumberTable: 
   line 4: 0
   line 5: 2
   line 6: 5
   line 7: 9
   line 8: 16
2.1.3. CPU缓存，L1，L2，L3和伪共享

http://duartes.org/gustavo/blog/post/intel-cpu-caches/

http://mechanical-sympathy.blogspot.com/2011/07/false-sharing.html

2.1.4. 什么是尾递归

2.1.5. 熟悉位运算

用位运算实现加、减、乘、除、取余

2.1.6. 参考资料

http://book.douban.com/subject/1138768/

http://book.douban.com/subject/6522893/

http://en.wikipedia.org/wiki/Java_class_file

http://en.wikipedia.org/wiki/Java_bytecode

http://en.wikipedia.org/wiki/Java_bytecode_instruction_listings

2.2. 设计模式

2.2.1. 实现AOP

CGLIB和InvocationHandler的区别 http://cglib.sourceforge.net/

动态代理模式 Javassist实现AOP http://www.csg.ci.i.u-tokyo.ac.jp/~chiba/javassist/

ASM实现AOP http://asm.ow2.org/

2.2.2. 使用模板方法设计模式和策略设计模式实现IOC

2.2.3. 不用synchronized和lock，实现线程安全的单例模式

2.2.4. nio和reactor设计模式

2.2.5. 参考资料

http://asm.ow2.org/

http://cglib.sourceforge.net/

http://www.javassist.org/

2.3. 网络编程知识

2.3.1. Java RMI，Socket，HttpClient

2.3.2. 用Java写一个简单的静态文件的HTTP服务器

实现客户端缓存功能，支持返回304 实现可并发下载一个文件 使用线程池处理客户端请求 使用nio处理客户端请求 支持简单的rewrite规则 上述功能在实现的时候需要满足“开闭原则”

2.3.3. 了解nginx和apache服务器的特性并搭建一个对应的服务器

http://nginx.org/

http://httpd.apache.org/

2.3.4. 用Java实现FTP、SMTP协议

2.3.5. 什么是CDN？如果实现？DNS起到什么作用？

搭建一个DNS服务器 搭建一个 Squid 或 Apache Traffic Server 服务器 http://www.squid-cache.org/ http://trafficserver.apache.org/ http://en.wikipedia.org/wiki/Domain_Name_System

2.3.6. 参考资料

http://www.ietf.org/rfc/rfc2616.txt

http://tools.ietf.org/rfc/rfc5321.txt

http://en.wikipedia.org/wiki/Open/closed_principle

2.4. 框架知识

spring，spring mvc，阅读主要源码 ibatis，阅读主要源码 用spring和ibatis搭建java server

2.5. 应用服务器知识

熟悉使用jboss，https://www.jboss.org/overview/ 熟悉使用tomcat，http://tomcat.apache.org/ 熟悉使用jetty，http://www.eclipse.org/jetty/
