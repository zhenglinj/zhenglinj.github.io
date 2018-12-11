---
typora-root-url: ../
title: "Java 从零进阶 - 语言基础"
categories: "technology"
tags:
  - java
---


《Java 从零进阶》系列将从：Java语言基础，JVM，并发编程三方面从介绍到深入理解Java。本文是该系列的语言基础篇。

---

## Java基础知识

- [Java入门教程](https://www.tutorialspoint.com/java/index.htm)  
- Java关键字
- [Java基本数据类型](http://www.runoob.com/java/java-basic-datatypes.html)  
- [Java String的使用](http://www.runoob.com/java/java-string.html)  
- [JDK源码](http://grepcode.com/snapshot/repository.grepcode.com/java/root/jdk/openjdk/8-b132/)  

开发环境教程：[IntelliJ IDEA 使用教程](http://wiki.jikexueyuan.com/project/intellij-idea-tutorial/)  

**基础包源代码**

> `java.lang.String` `java.lang.Integer` `java.lang.Long` `java.lang.Enum` `java.math.BigDecimal`
> `java.lang.ThreadLocal` `java.lang.ClassLoader` `java.net.URLClassLoader`

## Java集合框架

**Java集合框架**([参考这里](https://en.wikipedia.org/wiki/Java_collections_framework))用来表示和操作集合的统一框架，它包含接口，实现类以及一些编程辅助算法，具体位于`java.util`包下。[java.util 教程](https://www.tutorialspoint.com/java/util/index.htm)

Java集合框架(Java collections framework, JCF)是一组实现集合数据结构的类和接口。集合框架示意图如下(实际远比下图复杂)，图片来源于[这里](http://www.codejava.net/images/articles/javacore/collections/collections%20framework%20overview.png)

![Alt Text](/images/collections-framework-overview_thumb.png )

常用的集合类:
> `ArrayList` `LinkedList` `HashMap` `LinkedHashMap` `TreeMap` `HashSet` `LinkedHashSet` `TreeSet`

线程安全的集合类。`java.util.concurrent.*`包含许多线程安全、测试良好、高性能的并发构建块，目的就是要实现 Collection 框架对数据结构所执行的并发操作，性能优于`java.util.*`中的集合类：
> `ConcurrentHashMap` `CopyOnWriteArrayList` `CopyOnWriteArraySet` `ConcurrentLinkedDeque` `ConcurrentLinkedQueue` `ConcurrentSkipListMap` `ConcurrentSkipListSet`

> `Vector` `Collections.synchronizedCollection(...)` `Collections.synchronizedList(List)` `Collections.synchronizedMap(Map)` `Collections.synchronizedSet(Set)`  `Collections.synchronizedSortedSet(Set)` 

## Java IO 和 Java NIO

Java的IO操作中有面向字节(Byte)和面向字符(Character)两种方式。

- 面向字节的操作为以8位为单位对二进制的数据进行操作，对数据不进行转换，这些类都是InputStream和OutputStream的子类。
- 面向字符的操作为以字符为单位对数据进行操作，在读的时候将二进制数据转为字符，在写的时候将字符转为二进制数据，这些类都是Reader和Writer的子类。

总结：以InputStream（输入）/OutputStream（输出）为后缀的是字节流；以Reader（输入）/Writer（输出）为后缀的是字符流。Java流类图结构如下：

![Alt Text](/images/java_io_stream.jpg )

### Java NIO和IO的主要区别

| `java.io.*`    | `java.nio.*`         |
| :------------: | :------------------: |
| 面向流         | 面向缓冲             |
| 阻塞IO         | 非阻塞IO             |
| 无             | 选择器(Selectors)    |

参考 [Java NIO 入门](http://www.ibm.com/developerworks/cn/education/java/j-nio/j-nio.html) [Java NIO与IO](http://ifeve.com/java-nio-vs-io/)

### Reactor模式

IO并发设计：Reactor模式与Proactor模式

## Java特性

### Java反射与javassist

反射与工厂模式 `java.lang.reflect.*`

### Java序列化

什么是序列化，为什么序列化 序列化与单例模式 `java.io.Serializable`

定义了如下的Employee类，该类实现了 Serializable 接口

```java
public class Employee implements java.io.Serializable {
  public String name;
  public String address;
  public transient int SSN;
  public int number;

  public void mailCheck() {
    System.out.println("Mailing a check to " + name
          + " " + address);
  }
}
```

一个类的对象要想序列化必须满足两个条件：

- 该类必须实现 java.io.Serializable 对象。
- 该类的所有属性必须是可序列化的。如果有一个属性不是可序列化的，则该属性必须注明是短暂（transient）的。如果你想知道一个Java标准类是否是可序列化的，请查看该类的文档。检验一个类的实例是否能序列化十分简单， 只需要查看该类有没有实现java.io.Serializable接口。

**序列化和反序列化**

```java
import java.io.*;

public class Main {
  public static void main(String [] args) {
    String ser_filename = "./employee.ser";
    {
      // Serialize demo
      Employee e = new Employee();
      e.name = "Reyan Ali";
      e.address = "Phokka Kuan, Ambehta Peer";
      e.SSN = 11122333;
      e.number = 101;

      try {
        FileOutputStream fileOut =
                new FileOutputStream(ser_filename);
        ObjectOutputStream out = new ObjectOutputStream(fileOut);
        out.writeObject(e);
        out.close();
        fileOut.close();
        System.out.println("Serialized data is saved in " + ser_filename);
      } catch(IOException i) {
        i.printStackTrace();
      }
    }

    {
      // Deserialize demo
      Employee e = null;
      try {
        FileInputStream fileIn = new FileInputStream(ser_filename);
        ObjectInputStream in = new ObjectInputStream(fileIn);
        e = (Employee) in.readObject();
        in.close();
        fileIn.close();
      } catch(IOException i) {
        i.printStackTrace();
        return;
      } catch(ClassNotFoundException c) {
        System.out.println("Employee class not found");
        c.printStackTrace();
        return;
      }
      System.out.println("Deserialized Employee from " + ser_filename + " ..." );
      System.out.println("Name: " + e.name);
      System.out.println("Address: " + e.address);
      System.out.println("SSN: " + e.SSN);
      System.out.println("Number: " + e.number);
      e.mailCheck();
    }
  }
}
```

输出结果：

```markdown
Serialized data is saved in ./employee.ser
Deserialized Employee from ./employee.ser ...
Name: Reyan Ali
Address: Phokka Kuan, Ambehta Peer
SSN: 0
Number: 101
Mailing a check to Reyan Ali Phokka Kuan, Ambehta Peer
```

### 虚引用，弱引用，软引用

`java.lang.ref.*` 实验这些引用的回收

### Java系统属性

`java.util.Properties`

### Annotation用法

`java.lang.annotation.*`

### JMS

`javax.jms.*`

### JMX

`java.lang.management.*` `javax.management.*`

### 泛型和继承，泛型和擦除

### 自动拆箱装箱与字节码

### 实现Callback

### java.lang.Void类使用

### Java Agent，premain函数

`java.lang.instrument`

### 单元测试

[Junit](http://junit.org/)

[Jmockit](https://code.google.com/p/jmockit/)

[djUnit](http://works.dgic.co.jp/djunit/)

### Java正则表达式

Java实现通过正则表达式提取一段文本中的电子邮件，并将@替换为#输出

`java.lang.util.regex.*`

### 常用的Java工具库

`commons.lang` `commons.*...` `guava-libraries`

`guava` 是谷歌开源的Java标准包扩展项目

### API & SPI

[http://en.wikipedia.org/wiki/Application_programming_interface](http://en.wikipedia.org/wiki/Application_programming_interface)

[http://en.wikipedia.org/wiki/Service_provider_interface](http://en.wikipedia.org/wiki/Service_provider_interface)

### Apache Maven

[Apache Maven Project](http://maven.apache.org/index.html)
[IntelliJ IDEA中Maven功能](http://www.youmeek.com/intellij-idea-part-xviii-maven/)

### 参考资料

JDK src.zip 源代码

[http://openjdk.java.net/](http://openjdk.java.net/)

[http://commons.apache.org/](http://commons.apache.org/)

[https://code.google.com/p/guava-libraries/](https://code.google.com/p/guava-libraries/)

[http://netty.io/](http://netty.io/)

[http://stackoverflow.com/questions/2954372/difference-between-spi-and-api](http://stackoverflow.com/questions/2954372/difference-between-spi-and-api)

[http://stackoverflow.com/questions/11404230/how-to-implement-the-api-spi-pattern-in-java](http://stackoverflow.com/questions/11404230/how-to-implement-the-api-spi-pattern-in-java)
