---
typora-root-url: ../
title: "Java 从零进阶 - 并发编程"
categories: "technology"
tags: 
  - java
---


《Java 从零进阶》系列将从：Java语言基础，JVM，并发编程三方面从介绍到深入理解Java。本文是该系列的并发编程。

---

## Java并发编程

**线程的生命周期**

线程经过其生命周期的各个阶段。下图显示了一个线程完整的生命周期。

![Alt Text](/images/java_thread.jpg)

- 新状态：一个新产生的线程从新状态开始了它的生命周期。它保持这个状态知道程序start这个线程。
- 运行状态：当一个新状态的线程被start以后，线程就变成可运行状态，一个线程在此状态下被认为是开始执行其任务
- 就绪状态：当一个线程等待另外一个线程执行一个任务的时候，该线程就进入就绪状态。当另一个线程给就绪状态的线程发送信号时，该线程才重新切换到运行状态。
- 休眠状态：由于一个线程的时间片用完了，该线程从运行状态进入休眠状态。当时间间隔到期或者等待的时间发生了，该状态的线程切换到运行状态。
- 终止状态：一个运行状态的线程完成任务或者其他终止条件发生，该线程就切换到终止状态。

### 创建一个线程

Java提供了两种创建线程方法：

- 通过实现Runable接口，`java.lang.Runnable`  
- 通过继承Thread类本身，`java.lang.Thread`  

**通过实现Runnable接口来创建线程**

[ThreadDemo]({{site.postsurl}}/code/JavaThread/ThreadDemo.java)

**通过继承Thread来创建线程**

[ExtendThread]({{site.postsurl}}/code/JavaThread/ExtendThread.java)


## Java 多线程三大核心

### 原子性

`Java` 的原子性就和数据库事务的原子性差不多，一个操作中要么全部执行成功或者失败。

`JMM` 只是保证了基本的原子性，但类似于 `i++` 之类的操作，看似是原子操作，其实里面涉及到:

- 获取 i 的值。
- 自增。
- 再赋值给 i。

这三步操作，所以想要实现 `i++` 这样的原子操作就需要用到 `synchronized` 或者是 `lock` 进行加锁处理。

如果是基础类的自增操作可以使用 `AtomicInteger` 这样的原子类来实现(其本质是利用了 `CPU` 级别的 的 `CAS` 指令来完成的)。

其中用的最多的方法就是: `incrementAndGet()` 以原子的方式自增。
源码如下:

```java
public final long incrementAndGet() {
    for (;;) {
        long current = get();
        long next = current + 1;
        if (compareAndSet(current, next))
            return next;
    }
}
```

首先是获得当前的值，然后自增 +1。接着则是最核心的 `compareAndSet() ` 来进行原子更新。

```java
public final boolean compareAndSet(long expect, long update) {
    return unsafe.compareAndSwapLong(this, valueOffset, expect, update);
}
```

其逻辑就是判断当前的值是否被更新过，是否等于 `current`，如果等于就说明没有更新过然后将当前的值更新为 `next`，如果不等于则返回`false` 进入循环，直到更新成功为止。

还有其中的 `get()` 方法也很关键，返回的是当前的值，当前值用了 `volatile` 关键词修饰，保证了内存可见性。

```java
 private volatile int value;
```


### 可见性

现代计算机中，由于 `CPU` 直接从主内存中读取数据的效率不高，所以都会对应的 `CPU` 高速缓存，先将主内存中的数据读取到缓存中，线程修改数据之后首先更新到缓存，之后才会更新到主内存。如果此时还没有将数据更新到主内存其他的线程此时来读取就是修改之前的数据。

![](https://ws2.sinaimg.cn/large/006tKfTcly1fmouu3fpokj31ae0osjt1.jpg)

如上图所示。

`volatile` 关键字就是用于保证内存可见性，当线程A更新了 volatile 修饰的变量时，它会立即刷新到主线程，并且将其余缓存中该变量的值清空，导致其余线程只能去主内存读取最新值。

使用 `volatile` 关键词修饰的变量每次读取都会得到最新的数据，不管哪个线程对这个变量的修改都会立即刷新到主内存。

`synchronized`和加锁也能能保证可见性，实现原理就是在释放锁之前其余线程是访问不到这个共享变量的。但是和 `volatile` 相比开销较大。

### 顺序性

以下这段代码:

```java
int a = 100 ; //1
int b = 200 ; //2
int c = a + b ; //3
```

正常情况下的执行顺序应该是 `1>>2>>3`。但是有时 `JVM` 为了提高整体的效率会进行指令重排导致执行的顺序可能是 `2>>1>>3`。但是 `JVM` 也不能是什么都进行重排，是在保证最终结果和代码顺序执行结果一致的情况下才可能进行重排。

重排在单线程中不会出现问题，但在多线程中会出现数据不一致的问题。

Java 中可以使用 `volatile` 来保证顺序性，`synchronized 和 lock` 也可以来保证有序性，和保证原子性的方式一样，通过同一段时间只能一个线程访问来实现的。

除了通过 `volatile` 关键字显式的保证顺序之外， `JVM` 还通过 `happen-before` 原则来隐式的保证顺序性。

其中有一条就是适用于 `volatile` 关键字的，针对于 `volatile` 关键字的写操作肯定是在读操作之前，也就是说读取的值肯定是最新的。

#### volatile 的应用

**双重检查锁的单例模式**

可以用 `volatile` 实现一个双重检查锁的单例模式：

```java
public class Singleton {
    private static volatile Singleton singleton;

    private Singleton() {
    }

    public static Singleton getInstance() {
        if (singleton == null) {
            synchronized (Singleton.class) {
                if (singleton == null) {
                    singleton = new Singleton();
                }
            }
        }
        return singleton;
    }

}
```

这里的 `volatile` 关键字主要是为了防止指令重排。
如果不用 `volatile` ，`singleton = new Singleton();`，这段代码其实是分为三步：

- 分配内存空间。(1)
- 初始化对象。(2)
- 将 `singleton` 对象指向分配的内存地址。(3)

加上 `volatile` 是为了让以上的三步操作顺序执行，反之有可能第三步在第二步之前被执行就有可能导致某个线程拿到的单例对象还没有初始化，以致于使用报错。

**控制停止线程的标记**

```java
    private volatile boolean flag ;
    private void run(){
        new Thread(new Runnable() {
            @Override
            public void run() {
                doSomeThing();
            }
        });
    }

    private void stop(){
        flag = false ;
    }
```

这里如果没有用 volatile 来修饰 flag ，就有可能其中一个线程调用了 `stop()`方法修改了 flag 的值并不会立即刷新到主内存中，导致这个循环并不会立即停止。

这里主要利用的是 `volatile` 的内存可见性。

总结一下:
- `volatile` 关键字只能保证可见性，顺序性，**不能保证原子性**。

## java.util.concurrent

常用组件：

> Executor
> ExecutorService
> ScheduledExecutorService
> Future
> CountDownLatch
> CyclicBarrier
> Semaphore
> ThreadFactory
> BlockingQueue
> DelayQueue
> Locks
> Phaser

`CountDownLatch` 用法[Guide to CountDownLatch in Java](https://www.baeldung.com/java-countdown-latch)：
1. Waiting for a Pool of Threads to Complete,
2. A Pool of Threads Waiting to Begin.

[Overview of the java.util.concurrent](https://www.baeldung.com/java-util-concurrent)  
[Concurrency in JDK 5.0](https://www.ibm.com/developerworks/java/tutorials/j-concur/j-concur.html)  
[java.util.concurrent，第 1 部分](https://www.ibm.com/developerworks/cn/java/j-5things4/index.html)  
[java.util.concurrent，第 2 部分](https://www.ibm.com/developerworks/cn/java/j-5things5/index.html)  

## 使用线程池

自己设计线程池需要注意什么

## 线程安全

## 锁

什么是锁，锁的种类有哪些，每种锁有什么特点，适用场景是什么 在并发编程中锁的意义是什么

## synchronized和lock

synchronized的作用是什么

## sleep和wait

## wait和notify

## 什么是守护线程

守护线程和非守护线程的区别以及用法

## volatile关键字的理解

C++ volatile关键字和Java volatile关键字 happens-before语义 编译器指令重排和CPU指令重排

[http://en.wikipedia.org/wiki/Memory_ordering](http://en.wikipedia.org/wiki/Memory_ordering)

[http://en.wikipedia.org/wiki/Volatile_variable](http://en.wikipedia.org/wiki/Volatile_variable)

[java中volatile关键字的含义](http://www.cnblogs.com/aigongsi/archive/2012/04/01/2429166.html)

[Java 理论与实践: 正确使用Volatile 变量](http://www.ibm.com/developerworks/cn/java/j-jtp06197.html+&cd=2&hl=en&ct=clnk&gl=us)

[http://docs.oracle.com/javase/specs/jls/se7/html/jls-8.html#jls-8.3.1.4](http://docs.oracle.com/javase/specs/jls/se7/html/jls-8.html#jls-8.3.1.4)

[http://preshing.com/20130702/the-happens-before-relation/](http://preshing.com/20130702/the-happens-before-relation/)

## 线程安全

如果为count加上volatile修饰是否能够做到线程安全？你觉得该怎么做是线程安全的？

```java
public class Sample {
  private static int count = 0;
  public static void increment() {
    count++;
  }
}
```

解释一下下面两段代码的差别

```java
// 代码1
public class Sample {
  private static int count = 0;
  synchronized public static void increment() {
    count++;
  }
}
// 代码2
public class Sample {
  private static AtomicInteger count = new AtomicInteger(0);
  public static void increment() {
    count.getAndIncrement();
  }
}
```

## 参考资料

[http://book.douban.com/subject/10484692/](http://book.douban.com/subject/10484692/)

[http://www.intel.com/content/www/us/en/processors/architectures-software-developer-manuals.html](http://www.intel.com/content/www/us/en/processors/architectures-software-developer-manuals.html)
