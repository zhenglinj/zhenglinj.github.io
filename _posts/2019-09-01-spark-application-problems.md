---
typora-root-url: ../
analytics: true
comments: true
title: "Spark Application 开发遇到的问题"
categories: "technology"
tags:
  - spark
---

---

## Spark Applicaiton 开发遇到的问题

 本文基于：Java 1.8，Spark 1.6环境 

### Transform 线程安全问题





### NotSerializableException 异常分析及解决方法

在使用spark开发分布式数据计算作业过程中或多或少会遇到如下的错误：

```
org.apache.spark.SparkException: Task not serializable

	at org.apache.spark.util.ClosureCleaner$.ensureSerializable(ClosureCleaner.scala:304)
	at org.apache.spark.util.ClosureCleaner$.org$apache$spark$util$ClosureCleaner$$clean(ClosureCleaner.scala:294)
	at org.apache.spark.util.ClosureCleaner$.clean(ClosureCleaner.scala:122)
	at org.apache.spark.SparkContext.clean(SparkContext.scala:2055)
	at org.apache.spark.rdd.RDD$$anonfun$map$1.apply(RDD.scala:324)
	at org.apache.spark.rdd.RDD$$anonfun$map$1.apply(RDD.scala:323)
	at org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:150)
	at org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:111)
	at org.apache.spark.rdd.RDD.withScope(RDD.scala:316)
	at org.apache.spark.rdd.RDD.map(RDD.scala:323)
	at org.apache.spark.api.java.JavaRDDLike$class.map(JavaRDDLike.scala:96)
	at org.apache.spark.api.java.AbstractJavaRDDLike.map(JavaRDDLike.scala:46)
...
Caused by: java.io.NotSerializableException: ...
Serialization stack:
...
```

#### 分析

Spark处理的数据单元为RDD（即弹性分布式数据集），当我们对RDD进行一些transform操作（map,filter等操作）是由分布在不同机器上的executor来完成的。Spark不移动数据RDD，而是分布式地分发闭包算法。如果我们在driver中定义了一个变量，在map等操作中使用，则这个变量就要被分发到各个executor，因为driver和executor的运行在不同的jvm中，势必会涉及到对象的序列化与反序列化。如果这个变量没法序列化就会报异常。还有一种情况就是引用的对象可以序列化，但是引用的对象本身引用的其他对象无法序列化，也会有异常。

异常信息中Serialization stack给我们定位问题提供很多信息。

#### 解决方法

以下构造一个例子：

UnserializableClass没有继承Serializable接口，有成员函数method，静态成员函数staticMethod

```java
package com.spark.examples.unserializabledemo;

public class UnserializableClass {
    public int method(int x) {
        return x * x;
    }

    public static int staticMethod(int x) {
        return x * x;
    }
}
```

写一个测试类，如下：

```java
package com.spark.examples.unserializabledemo;

import org.apache.spark.SparkConf;
import org.apache.spark.SparkContext;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import java.util.Arrays;

public class SparkSerializableTest {
    private static SparkContext sc;

    private static JavaSparkContext jsc;

    @BeforeClass
    public static void beforeClass() {
        SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("test");

        SparkContext sc = new SparkContext(conf);
        jsc = JavaSparkContext.fromSparkContext(sc);
    }

    @AfterClass
    public static void afterClass() {
        jsc.close();
    }

    @Test(expected = org.apache.spark.SparkException.class)
    public void testUnserializableClassMethod() {
        JavaRDD<Integer> javaRDD = jsc.parallelize(Arrays.asList(1, 2, 3, 4, 5));
        UnserializableClass unserializableClass = new UnserializableClass();
        javaRDD.map(x -> unserializableClass.method(x)).collect().forEach(System.out::println);
    }

    @Test(expected = org.apache.spark.SparkException.class)
    public void testUnserializableClassObjectStaticMethod() {
        JavaRDD<Integer> javaRDD = jsc.parallelize(Arrays.asList(1, 2, 3, 4, 5));
        UnserializableClass unserializableClass = new UnserializableClass();
        javaRDD.map(x -> unserializableClass.staticMethod(x)).collect().forEach(System.out::println);
    }
}
```

第一个第二个测试用例会报错，如下Serialization stack信息：

```
Serialization stack:
	- object not serializable (class: com.spark.examples.unserializabledemo.UnserializableClass, value: com.spark.examples.unserializabledemo.UnserializableClass@3e1624c7)
	- element of array (index: 0)
	- array (class [Ljava.lang.Object;, size 1)
	- field (class: java.lang.invoke.SerializedLambda, name: capturedArgs, type: class [Ljava.lang.Object;)
	- object (class java.lang.invoke.SerializedLambda, SerializedLambda[capturingClass=class com.spark.examples.unserializabledemo.SparkNotSerializableExceptionTest, functionalInterfaceMethod=org/apache/spark/api/java/function/Function.call:(Ljava/lang/Object;)Ljava/lang/Object;, implementation=invokeStatic com/spark/examples/unserializabledemo/SparkNotSerializableExceptionTest.lambda$testUnserializableClassMethod$281dca3f$1:(Lcom/spark/examples/unserializabledemo/UnserializableClass;Ljava/lang/Integer;)Ljava/lang/Integer;, instantiatedMethodType=(Ljava/lang/Integer;)Ljava/lang/Integer;, numCaptured=1])
	- writeReplace data (class: java.lang.invoke.SerializedLambda)
	- object (class com.spark.examples.unserializabledemo.SparkNotSerializableExceptionTest$$Lambda$3/26418585, com.spark.examples.unserializabledemo.SparkNotSerializableExceptionTest$$Lambda$3/26418585@2a1debfa)
	- field (class: org.apache.spark.api.java.JavaPairRDD$$anonfun$toScalaFunction$1, name: fun$1, type: interface org.apache.spark.api.java.function.Function)
	- object (class org.apache.spark.api.java.JavaPairRDD$$anonfun$toScalaFunction$1, <function1>)
```

由Serialization stack信息定位到我们调用UnserializableClass类对象方法时出错，相应修改办法：

- 将不可序列化的对象定义在闭包内

  ```java
  @Test
  public void testNewUnserializableClassMethod() {
      JavaRDD<Integer> javaRDD = jsc.parallelize(Arrays.asList(1, 2, 3, 4, 5));
      javaRDD.map(x -> new UnserializableClass().method(x)).collect().forEach(System.out::println);
  }
  ```

  

- 使用static修饰方法，即将方法改成类方法，如下代码。使用static或transient修饰不可序列化的属性从而避免序列化

  ```java
  @Test
  public void testUnserializableClassStaticMethod() {
      JavaRDD<Integer> javaRDD = jsc.parallelize(Arrays.asList(1, 2, 3, 4, 5));
      javaRDD.map(x -> UnserializableClass.staticMethod(x)).collect().forEach(System.out::println);
  }
  ```

  

- 给无法序列化的类加上java.io.Serializable接口，如下代码：

  ```java
  package com.spark.examples.unserializabledemo;
   
  public class SerializableClass implements java.io.Serializable {
      public int method(int x) {
          return x * x;
      }
  }
  ```

  

**注册序列化类无法解决NotSerializableException问题**

```java
package com.spark.examples.unserializabledemo;

import com.spark.examples.unserializabledemo.util.SerializableClass;
import com.spark.examples.unserializabledemo.util.UnserializableClass;
import org.apache.spark.SparkConf;
import org.apache.spark.SparkContext;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import java.io.IOException;
import java.util.Arrays;

public class SparkSerializableKryoTest {
    private static JavaSparkContext jsc;

    @BeforeClass
    public static void beforeClass() {
        SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("test");

        // 使用Kryo序列化库
        conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer");
        // 在Kryo序列化库中注册自定义的类集合
        conf.registerKryoClasses(new Class[] {
                com.spark.examples.unserializabledemo.util.UnserializableClass.class,
                com.spark.examples.unserializabledemo.util.SerializableClass.class
        });

        SparkContext sc = new SparkContext(conf);
        jsc = JavaSparkContext.fromSparkContext(sc);
    }

    @AfterClass
    public static void afterClass() {
        jsc.close();
    }

    @Test(expected = org.apache.spark.SparkException.class)
    public void testUnserializableClassMethod() throws IOException {
        JavaRDD<Integer> javaRDD = jsc.parallelize(Arrays.asList(1, 2, 3, 4, 5));
        UnserializableClass unserializableClass = new UnserializableClass();
        javaRDD.map(x -> unserializableClass.method(x)).collect().forEach(System.out::println);
    }

    @Test
    public void testSerializableClassMethod() throws IOException {
        JavaRDD<Integer> javaRDD = jsc.parallelize(Arrays.asList(1, 2, 3, 4, 5));
        SerializableClass serializableClass = new SerializableClass();
        javaRDD.map(x -> serializableClass.method(x)).collect().forEach(System.out::println);
    }
}
```


### Lambda表达式序列化问题

问题起因：使用Spark的Java接口做filter操作的过程中，遇到了匪夷所思的错误，问题大概可以抽象成下面一段代码：

```java
@Test
public void testFilter() throws Exception{
    SparkConf conf = new SparkConf()
        .setMaster("local[*]")
        .setAppName("test");
    JavaSparkContext context = new JavaSparkContext(conf);

    List<String> list1 = Arrays.asList("a", "b", null, "c");
    List<Integer> list2 = Arrays.asList(1, 2, null, 3);
    context.parallelize(list1)
        .filter(Objects::nonNull);

    context.parallelize(list2)
        .filter(Objects::nonNull)
        // System.out::println 会报Serializable Issue
        .foreach(a -> System.out.println(a));
}
```

这段代码中创建了两个List，一个String的，一个Integer的，然后调用java.util.Objects.nonNull()方法分别执行过滤掉null的逻辑。

这段代码是能够通过编译的，但是一旦运行，就会出现下面的异常：

```text
 java.lang.ClassCastException: java.lang.Integer cannot be cast to java.lang.String
	at org.apache.spark.api.java.JavaRDD$$anonfun$filter$1.apply(JavaRDD.scala:76)
```

可以看到，在list1上的过滤操作甚至都没有真正执行（没有使用Spark的shuffle操作），那么这个问题是怎么产生的呢？最初怀疑是method-ref的引用问题，是不是说在method-ref委派的过程中，由于应用到的类型不同，产生了二义性问题呢？使用下面的代码测试：

```java
@Test
public void testBasicFilter() {
    List<String> list1 = Arrays.asList("a", "b", null, "c");
    List<Integer> list2 = Arrays.asList(1, 2, null, 3);
    list1.stream()
        .filter(Objects::nonNull)
        .forEach(System.out::println);

    list2.stream()
        .filter(Objects::nonNull)
        .forEach(System.out::println);
}
```

这段代码使用JDK自带的stream替代Spark进行相同的逻辑，结果是不但正确通过编译，执行结果也正常，执行结果如下：

```text
a
b
c
1
2
3
```

这就否定了之前的假设，那么究竟是什么导致了异常呢？仔细思考，Java8的Stream和Spark究竟有什么本质的不同呢：都是并行处理框架，**但是Spark是分布式的，分布式的涉及到网络传输，这必然涉及到数据处理任务可能会通过网络进行传输**（Spark确实会把任务广播到各个节点上），因此一定会涉及到Task的**序列化**，会不会是序列化出现了问题？

为了验证这个猜测，构造了如下的代码：

```java
import org.apache.commons.lang3.SerializationUtils;
import org.junit.Test;

import java.io.Serializable;
import java.util.Objects;
import java.util.function.Function;

public class LambdaSerializationTest {
    private static <T> T roundtrip(Serializable obj) {
        byte[] bytes = SerializationUtils.serialize(obj);
        @SuppressWarnings("unchecked")
        T t = (T) SerializationUtils.deserialize(bytes);
        return t;
    }

    @Test
    public void test() {
        SerializableFunction<Integer, Boolean> func = Objects::nonNull;
        System.out.println(func.apply(1));
        SerializableFunction<String, Boolean> fun1 = roundtrip(func);
        System.out.println(fun1.apply("a"));
    }

    private interface SerializableFunction<T, R> extends Function<T, R>, Serializable {
    }
}
```

这段代码先将Objects::nonNull向下转为Function<Integer,Boolean>类型

反序列化回来的过程中反序列化为Function<String,Boolean>类型

Object.nonNull()方法的原型如下：

```java
    /**
     * Returns {@code true} if the provided reference is non-{@code null}
     * otherwise returns {@code false}.
     *
     * @apiNote This method exists to be used as a
     * {@link java.util.function.Predicate}, {@code filter(Objects::nonNull)}
     *
     * @param obj a reference to be checked against {@code null}
     * @return {@code true} if the provided reference is non-{@code null}
     * otherwise {@code false}
     *
     * @see java.util.function.Predicate
     * @since 1.8
     */
    public static boolean nonNull(Object obj) {
        return obj != null;
    }
```

所以对类型是没有要求的，是不是说明这段代码可以正确运行呢？我们执行这段代码：

```text
true

java.lang.ClassCastException: java.lang.String cannot be cast to java.lang.Integer

	...
```

java.lang.ClassCastException重现了。

这说明：

**lambda表达式在序列化的过程中，不同于Java泛型的运行时擦除机制，会对类型进行特化，序列化前后的lambda表达式是携带类型信息的。**

之后我又参考了R大在知乎上[关于Lambda表达式与序列化的一个回答](https://www.zhihu.com/question/51491241/answer/126232275)，证明了之前的假设。

问题解决：

在Spark中，同一个method-ref可能会绑定到同一个serializable lambda，再次重用如果类型不匹配就会引发异常；如果使用匿名函数的形式，匿名函数可以匹配到对应的类型，类型不同对应就是两个serializable lambda，因此不会引发问题。

```text
Objects::nonNull =>    str -> str != null
Objects::nonNull =>    int -> int != null
```



Ref: [Java8 Lambda表达式序列化踩坑记]( https://zhuanlan.zhihu.com/p/37995638 )



### 爆内存相关问题汇总及解决

#### OOM

```
# 包括GC Overhead limitjava.lang.OutOfMemoryError 

# on yarn
org.apache.hadoop.yarn.server.nodemanager.containermanager.monitor.ContainersMonitorImpl  - Container [<edited>] is running beyond physical memory limits. Current usage: 18.0 GB of 18 GB physical memory used; 19.4 GB of 37.8 GB virtual memory used. Killing container.

Container exit code: 137
Task process exit with nonzero status of 137.
```

除了 `exit code 137` 外其它OOM提示都很明显，yarn container 137退出码按照SO的大神说：“Exit code 137 is a typical sign of the infamous OOM killer.”

解决方法：

- 加 executor 内存（spark.executor.memory），需注意on yarn时进程是按最小container memory的整数倍分配的。
- 优化程序内存占用
- 设置StorageLevel 到 DISK 或 MEMORY AND DISK，要注意persist只在action执行才生效，所以建议先count或isEmpty一下触发persist，然后再去做自己的flatMap/foreach等业务操作

Ref: [hadoop-streaming-job-failure-task-process-exit-with-nonzero-status-of-137](http://stackoverflow.com/questions/7312125/hadoop-streaming-job-failure-task-process-exit-with-nonzero-status-of-137) 

#### Shuffle Read OOM

```text
org.apache.spark.shuffle.MetadataFetchFailedException: Missing an output location for shuffle 0

org.apache.spark.shuffle.FetchFailedException: Failed to connect to ip-xxxxxxxx

org.apache.spark.shuffle.FetchFailedException: Error in opening FileSegmentManagedBuffer

java.io.FileNotFoundException of shuffle files in HDFS/S3
```

以上皆为可能的报错（但不代表报错一定就是OOM相关，要去找cause的exception；OOM不过是其中一种可能的cause），大致原因是shuffle后的executor读取数据超出了内存限制，然后挂了并且清除了相关的中间临时文件，其他的executor在尝试与其进行数据沟通时，要么executor丢失，要么无法读取其写出的shuffle文件等。当然FetchFailedException还有可能是其他原因，譬如某台机太繁忙无法响应等，这种情况可以尝试调整相关timeout参数进行尝试： spark.shuffle.io.maxRetries=6 ，spark.files.fetchTimeout=120s 。

如果你的单个shuffle block超过2g，然后又报类似以上列举的错误，你可能遭遇了以下 issue ： 

- [SPARK-5928 Remote Shuffle Blocks cannot be more than 2 GB ](https://issues.apache.org/jira/browse/SPARK-5928)
- [SPARK-1476 2GB limit in spark for blocks](https://issues.apache.org/jira/browse/SPARK-1476)

解决办法：

- 调大 repartition 数，减少每个repartition的size
- 调大executor内存
- on yarn的需调大 [spark.executor.overheadMemory](https://spark.apache.org/docs/1.6.2/running-on-yarn.html#spark-properties)，按SO的说法，需要自己根据实际情况测试调到不报错为止
- 根据实际情况调整 [spark.shuffle](https://spark.apache.org/docs/1.6.2/configuration.html#shuffle-behavior) 的相关参数。shuffle参数中大多数是关于shuffle write和shuflling的配置，而且基本大多数默认都是比较优的配置了。唯一shuffle read相关的`spark.reducer.maxMbInFlight`涉及源码参见 [Spark技术内幕: Shuffle详解（二）](http://blog.csdn.net/anzhsoft/article/details/41620329) ，因为shuffle fetch阶段是边fetch边处理的，所以适当调小该值有助于改善shuffle阶段的内存占用。 [shuffle部分参数说明](http://blog.csdn.net/gaowenhui2008/article/details/44452975)
- 有可能也是你物理内存不够了，增加可用内存吧
- 优化数据结构使用，尽量使用原始类型和数组，泛型和对象会造成较大的传输和存储开销。可考虑利用一些高效的序列化方案，比如protostuff。

Ref：

[what-are-the-likely-causes-of-org-apache-spark-shuffle-metadatafetchfailedexcept](http://stackoverflow.com/questions/29850784/what-are-the-likely-causes-of-org-apache-spark-shuffle-metadatafetchfailedexcept)

[fetchfailedexception-or-metadatafetchfailedexception-when-processing-big-data-set](http://stackoverflow.com/questions/34941410/fetchfailedexception-or-metadatafetchfailedexception-when-processing-big-data-set)

#### Streaming OOM

```
java.lang.Exception: Could not compute split, block input-0-1412705397200 not found 
```

Spark Streaming 中此错误产生原因是streaming产生了堆积，超过了receiver可承受的内存大小，因此旧的未执行的job被删除来去接收新的job。

解决方法：

- 调大 receiver 内存
- kafka 直接消费没有做rdd transform的可考虑换 [direct stream](https://spark.apache.org/docs/1.6.2/streaming-kafka-integration.html#approach-2-direct-approach-no-receivers) ，防止堆积。
- spark 1.6.x 可采用 [spark.streaming.backpressure.enabled](https://spark.apache.org/docs/1.6.2/configuration.html#spark-streaming) 机制回压，控制接收速率，防止爆内存。SparkConf设置 `spark.streaming.backpressure.enabled=true`, `spark.streaming.backpressure.pid.minrate=0.001`

Ref: 

- [Spark Streaming : Could not compute split, block not found](http://apache-spark-user-list.1001560.n3.nabble.com/Spark-Streaming-Could-not-compute-split-block-not-found-td11186.html)
- [could-not-compute-split-block-not-found](https://qnalist.com/questions/4988059/could-not-compute-split-block-not-found)

#### Insufficient Physical Memory

```
There is insufficient memory for the Java Runtime Environment to continue.
Native memory allocation (malloc) failed to allocate 4088 bytes for AllocateHeap
An error report file with more information is saved as:
```

其实就是没有足够的物理内存去启动这个JVM了，比如你JVM申请5g，实际只剩下4g可用的物理内存，就会报错，然后jvm启动失败进程退出。

解决方法：

- 加物理内存
- 优化程序和数据结构，调低jvm内存需求
- kill掉其他占用系统内存进程释放可用内存

问题：这里的可用内存包不包括操作系统cache的内存呢？ （`free -m` 可查看OS的free和cached内存）

Ref : [insufficient-memory-for-the-java-runtime-environment-message-in-eclipse](http://stackoverflow.com/questions/22805552/insufficient-memory-for-the-java-runtime-environment-message-in-eclipse)

#### 爆内存相关问题小结

其实以上的很多解决办法基本是OOM大多数问题通用的，比如持久化、内存调大、数据结构优化。

如果以上问题还不能解决，请参考：http://spark.apache.org/docs/latest/tuning.html 中的 Memory Tuning部分