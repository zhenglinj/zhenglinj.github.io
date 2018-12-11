---
typora-root-url: ../
title: "Java 从零进阶 - JVM"
categories: "technology"
tags:
  - java
---


《Java 从零进阶》系列将从：Java语言基础，JVM，并发编程三方面从介绍到深入理解Java。本文是该系列的JVM。

---

## Java虚拟机JVM

## Java内存模型

[http://www.jcp.org/en/jsr/detail?id=133](http://www.jcp.org/en/jsr/detail?id=133)  
[Java内存模型FAQ](http://ifeve.com/jmm-faq/)  

## Java内存管理，堆和栈

## Java垃圾回收机制

[深入理解java垃圾回收机制](http://www.cnblogs.com/sunniest/p/4575144.html)  


[深入理解JVM(2)——GC算法与内存分配策略](https://crowhawk.github.io/2017/08/10/jvm_2/)  

### JVM垃圾收集器

[深入理解JVM(3)——7种垃圾收集器](https://crowhawk.github.io/2017/08/15/jvm_3/)  

| 收集器            | 串行、并行or并发 | 新生代/老年代 | 算法               | 目标         | 适用场景                                  |
|-------------------|------------------|---------------|--------------------|--------------|-------------------------------------------|
| Serial            | 串行             | 新生代        | 复制算法           | 响应速度优先 | 单CPU环境下的Client模式                   |
| Serial Old        | 串行             | 老年代        | 标记-整理          | 响应速度优先 | 单CPU环境下的Client模式、CMS的后备预案    |
| ParNew            | 并行             | 新生代        | 复制算法           | 响应速度优先 | 多CPU环境时在Server模式下与CMS配合        |
| Parallel Scavenge | 并行             | 新生代        | 复制算法           | 吞吐量优先   | 在后台运算而不需要太多交互的任务          |
| Parallel Old      | 并行             | 老年代        | 标记-整理          | 吞吐量优先   | 在后台运算而不需要太多交互的任务          |
| CMS               | 并发             | 老年代        | 标记-清除          | 响应速度优先 | 集中在互联网站或B/S系统服务端上的Java应用 |
| G1                | 并发             | both          | 标记-整理+复制算法 | 响应速度优先 | 面向服务端应用，将来替换CMS               |

## JVM类加载

[深入理解JVM(5)——虚拟机类加载机制](https://crowhawk.github.io/2017/08/21/jvm_5/)  
[深入理解JVM(6)——类加载器](https://crowhawk.github.io/2017/08/21/jvm_6/)  

## JVM各种参数及调优

## Java工具的使用

jps, jstack, jmap, jconsole, jinfo, jhat, javap, …

[http://kenai.com/projects/btrace](http://kenai.com/projects/btrace)

[http://www.crashub.org/](http://www.crashub.org/)

[https://github.com/taobao/TProfiler](https://github.com/taobao/TProfiler)

[https://github.com/CSUG/HouseMD](https://github.com/CSUG/HouseMD)

[http://wiki.cyclopsgroup.org/jmxterm](http://wiki.cyclopsgroup.org/jmxterm)

[https://github.com/jlusdy/TBJMap](https://github.com/jlusdy/TBJMap)

## Java诊断工具

[http://www.eclipse.org/mat/](http://www.eclipse.org/mat/)

[http://visualvm.java.net/oqlhelp.html](http://visualvm.java.net/oqlhelp.html)

**编写OutOfMemory, StackOverFlow程序**

> Heap OutOfMemory  
> Young OutOfMemory  
> MethodArea OutOfMemory  
> ConstantPool OutOfMemory  
> DirectMemory OutOfMemory  
> Stack OutOfMemory  
> Stack OverFlow  

[https://plumbr.eu/blog/memory-leaks/understanding-java-lang-outofmemoryerror](https://plumbr.eu/blog/memory-leaks/understanding-java-lang-outofmemoryerror)

**使用工具尝试解决以下问题，并写下总结**

当一个Java程序响应很慢时如何查找问题 当一个Java程序频繁FullGC时如何解决问题，如何查看垃圾回收日志 当一个Java应用发生OutOfMemory时该如何解决，年轻代、年老代、永久代解决办法不同，导致原因也不同

## 参考资料

[http://docs.oracle.com/javase/specs/jvms/se7/html/](http://docs.oracle.com/javase/specs/jvms/se7/html/)

[http://www.cs.umd.edu/~pugh/java/memoryModel/](http://www.cs.umd.edu/~pugh/java/memoryModel/)

[http://gee.cs.oswego.edu/dl/jmm/cookbook.html](http://gee.cs.oswego.edu/dl/jmm/cookbook.html)
