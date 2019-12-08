---
typora-root-url: ../
analytics: true
comments: true
title: "优化Spark作业以获得最佳性能"
categories: "technology"
tags:
  - spark
---

---

# 优化Spark作业以获得最佳性能

[原文](https://michalsenkyr.github.io/2018/01/spark-performance#dataframes-and-datasets)

---

从表面上看，Spark作业的开发似乎很容易，而且在大多数情况下确实如此。所提供的API设计精良且功能丰富，如果您熟悉Scala集合或Java流，那么您将很快完成实现。在群集上并在满负载下运行它们时，真正困难的部分是，因为并非所有作业在性能上都是相同的。不幸的是，要以最佳方式实施您的工作，您必须对Spark及其内部有相当的了解。

在本文中，我将讨论开发Spark应用程序时可能遇到的最常见的性能问题，以及如何避免或减轻它们。

![标题图片](https://michalsenkyr.github.io/images/2018-01-04-spark-performance/title.jpg)

## 1.转换 Transformations

使用RDD API时，最常见的性能问题是使用的转换对于特定用例而言是不够的。这可能是由于许多用户熟悉SQL查询语言及其对查询优化的依赖。重要的是要认识到RDD API不会应用任何此类优化。

让我们看一下相同计算的以下两个定义：

```scala
val input = sc.parallelize(1 to 10000000, 42).map(x => (x % 42, x))
val definition1 = input.groupByKey().mapValues(_.sum)
val definition2 = input.reduceByKey(_ + _)
```

| RDD   | 平均时间 | Min时间 | Max时间 |
| :---- | -------: | ------: | ------: |
| 定义1 | 2646.3ms |  1570ms |  8444ms |
| 定义2 |  270.7ms |    96ms |  1569ms |

**Lineage （definition1）：**

```
(42) MapPartitionsRDD[3] at mapValues at <console>:26 []
 |   ShuffledRDD[2] at groupByKey at <console>:26 []
 +-(42) MapPartitionsRDD[1] at map at <console>:24 []
    |   ParallelCollectionRDD[0] at parallelize at <console>:24 []
```

**Lineage （definition2）：**

```
(42) ShuffledRDD[4] at reduceByKey at <console>:26 []
 +-(42) MapPartitionsRDD[1] at map at <console>:24 []
    |   ParallelCollectionRDD[0] at parallelize at <console>:24 []
```

第二个定义比第一个定义快得多，因为它在我们的用例环境中通过不不必要地收集所有元素来更有效地处理数据。

在进行笛卡尔联接并随后对结果数据进行过滤而不是转换为RDD对并使用内部联接时，我们可以观察到类似的性能问题：

```scala
val input1 = sc.parallelize(1 to 10000, 42)
val input2 = sc.parallelize(1.to(100000, 17), 42)
val definition1 = input1.cartesian(input2).filter { case (x1, x2) => x1 % 42 == x2 % 42 }
val definition2 = input1.map(x => (x % 42, x)).join(input2.map(x => (x % 42, x))).map(_._2)
```

| RDD   | 平均时间 | Min时间 | Max时间 |
| :---- | -------: | ------: | ------: |
| 定义1 | 9255.3ms |  3750ms | 12077ms |
| 定义2 |   1525ms |   623ms |  2759ms |

**Lineage （definition1）：**

```
(1764) MapPartitionsRDD[34] at filter at <console>:30 []
  |    CartesianRDD[33] at cartesian at <console>:30 []
  |    ParallelCollectionRDD[0] at parallelize at <console>:24 []
  |    ParallelCollectionRDD[1] at parallelize at <console>:24 []
```

**Lineage （definition2）：**

```
(42) MapPartitionsRDD[40] at map at <console>:30 []
 |   MapPartitionsRDD[39] at join at <console>:30 []
 |   MapPartitionsRDD[38] at join at <console>:30 []
 |   CoGroupedRDD[37] at join at <console>:30 []
 +-(42) MapPartitionsRDD[35] at map at <console>:30 []
 |  |   ParallelCollectionRDD[0] at parallelize at <console>:24 []
 +-(42) MapPartitionsRDD[36] at map at <console>:30 []
    |   ParallelCollectionRDD[1] at parallelize at <console>:24 []
```

经验法则是始终在转换边界处使用最少的数据量。RDD API会尽其所能来优化后台工作，例如任务调度，基于数据局部性的首选位置等。但它不会优化计算本身。实际上，这样做实际上是不可能的，因为每个转换都是由一个不透明的函数定义的，Spark无法查看我们正在使用的数据以及如何处理。

由此可以得出另一条经验法则：使用丰富的转换，即始终在单个转换的上下文中尽可能多地执行操作。用于此目的的有用工具是[`combineByKeyWithClassTag`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.rdd.PairRDDFunctions@combineByKeyWithClassTag[C](createCombiner:V=>C,mergeValue:(C,V)=>C,mergeCombiners:(C,C)=>C)(implicitct:scala.reflect.ClassTag[C]):org.apache.spark.rdd.RDD[(K,C)])：

```scala
val input = sc.parallelize(1 to 1000000, 42).keyBy(_ % 1000)
val combined = input.combineByKeyWithClassTag((x: Int) => Set(x / 1000), (s: Set[Int], x: Int) => s + x / 1000, (s1: Set[Int], s2: Set[Int]) => s1 ++ s2)
```

**Lineage ：**

```
(42) ShuffledRDD[61] at combineByKeyWithClassTag at <console>:28 []
 +-(42) MapPartitionsRDD[57] at keyBy at <console>:25 []
    |   ParallelCollectionRDD[56] at parallelize at <console>:25 []
```

### DateFrames and DataSets

Spark社区实际上认识到了这些问题，并开发了两组高级API来解决此问题：[DataFrame和Dataset](https://spark.apache.org/docs/latest/sql-programming-guide.html#datasets-and-dataframes)。这些API附带了有关数据的其他信息，并定义了在整个框架中都可以识别的特定转换。调用动作时，将对计算图进行最优化，并将其转换为相应的RDD图，然后执行该图。

为了演示，我们可以尝试用两种非常不同的方式定义两个等效的计算，并比较它们的运行时间和作业图：

```scala
val input1 = sc.parallelize(1 to 10000, 42).toDF("value1")
val input2 = sc.parallelize(1.to(100000, 17), 42).toDF("value2")
val definition1 = input1.crossJoin(input2).where('value1 % 42 === 'value2 % 42)
val definition2 = input1.join(input2, 'value1 % 42 === 'value2 % 42)
```

| 数据框 | 平均时间 | Min时间 | Max时间 |
| :----- | -------: | ------: | ------: |
| 定义1  | 1598.3ms |   929ms |  2765ms |
| 定义2  | 1770.9ms |   744ms |  2954ms |

**解析的逻辑计划（定义1）：**

```
'Filter (('value1 % 42) = ('value2 % 42))
+- Join Cross
   :- Project [value#2 AS value1#4]
   :  +- SerializeFromObject [input[0, int, false] AS value#2]
   :     +- ExternalRDD [obj#1]
   +- Project [value#9 AS value2#11]
      +- SerializeFromObject [input[0, int, false] AS value#9]
         +- ExternalRDD [obj#8]
```

**解析的逻辑计划（定义2）：**

```
Join Inner, ((value1#4 % 42) = (value2#11 % 42))
:- Project [value#2 AS value1#4]
:  +- SerializeFromObject [input[0, int, false] AS value#2]
:     +- ExternalRDD [obj#1]
+- Project [value#9 AS value2#11]
   +- SerializeFromObject [input[0, int, false] AS value#9]
      +- ExternalRDD [obj#8]
```

**物理计划（定义1）：**

```
*SortMergeJoin [(value1#4 % 42)], [(value2#11 % 42)], Cross
:- *Sort [(value1#4 % 42) ASC NULLS FIRST], false, 0
:  +- Exchange hashpartitioning((value1#4 % 42), 200)
:     +- *Project [value#2 AS value1#4]
:        +- *SerializeFromObject [input[0, int, false] AS value#2]
:           +- Scan ExternalRDDScan[obj#1]
+- *Sort [(value2#11 % 42) ASC NULLS FIRST], false, 0
   +- Exchange hashpartitioning((value2#11 % 42), 200)
      +- *Project [value#9 AS value2#11]
         +- *SerializeFromObject [input[0, int, false] AS value#9]
            +- Scan ExternalRDDScan[obj#8]
```

**物理计划（定义2）：**

```
*SortMergeJoin [(value1#4 % 42)], [(value2#11 % 42)], Inner
:- *Sort [(value1#4 % 42) ASC NULLS FIRST], false, 0
:  +- Exchange hashpartitioning((value1#4 % 42), 200)
:     +- *Project [value#2 AS value1#4]
:        +- *SerializeFromObject [input[0, int, false] AS value#2]
:           +- Scan ExternalRDDScan[obj#1]
+- *Sort [(value2#11 % 42) ASC NULLS FIRST], false, 0
   +- Exchange hashpartitioning((value2#11 % 42), 200)
      +- *Project [value#9 AS value2#11]
         +- *SerializeFromObject [input[0, int, false] AS value#9]
            +- Scan ExternalRDDScan[obj#8]
```

优化后，转换的原始类型和顺序无关紧要，这要归功于称为基于规则的查询优化的功能。由于基于成本的查询优化，还考虑了数据大小以正确的方式对作业进行重新排序。最后，DataFrame API还将有关作业实际需要的列的信息推送到数据源读取器，以限制输入读取（这称为谓词下推）。实际上，以与DataFrame API所提供的功能相当的方式编写RDD作业非常困难。

但是，在一个方面，DataFrames表现不佳，并促使创建了另一种表示Spark计算的方法：类型安全。由于仅出于转换定义的目的用名称表示数据列，并且仅在运行时检查它们在实际数据类型方面的有效用法，因此这往往导致冗长的开发过程，我们需要跟踪所有列正确的类型，否则我们在执行过程中会出错。创建数据集API就是为此的解决方案。

Dataset API使用Scala的类型推断和基于隐式的技术来传递[Encoders](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Encoder)，这是特殊的类，用于描述Spark优化器的数据类型，就像DataFrames一样，同时保留编译时类型以进行类型检查和编写转换自然。如果这听起来很复杂，请参考以下示例：

```scala
val input = sc.parallelize(1 to 10000000, 42)
val definition = input.toDS.groupByKey(_ % 42).reduceGroups(_ + _)
```

| 数据集 | 平均时间 | Min时间 | Max时间 |
| :----- | -------: | ------: | ------: |
| 定义   |  544.9ms |   472ms |   728ms |

**解析的逻辑计划：**

```
'Aggregate [value#301], [value#301, unresolvedalias(reduceaggregator(org.apache.spark.sql.expressions.ReduceAggregator@1d490b2b, Some(unresolveddeserializer(upcast(getcolumnbyordinal(0, IntegerType), IntegerType, - root class: "scala.Int"), value#298)), Some(int), Some(StructType(StructField(value,IntegerType,false))), input[0, scala.Tuple2, true]._1 AS value#303, input[0, scala.Tuple2, true]._2 AS value#304, newInstance(class scala.Tuple2), input[0, int, false] AS value#296, IntegerType, false, 0, 0), Some(<function1>))]
+- AppendColumns <function1>, int, [StructField(value,IntegerType,false)], cast(value#298 as int), [input[0, int, false] AS value#301]
   +- SerializeFromObject [input[0, int, false] AS value#298]
      +- ExternalRDD [obj#297]
```

**物理计划：**

```
ObjectHashAggregate(keys=[value#301], functions=[reduceaggregator(org.apache.spark.sql.expressions.ReduceAggregator@1d490b2b, Some(value#298), Some(int), Some(StructType(StructField(value,IntegerType,false))), input[0, scala.Tuple2, true]._1 AS value#303, input[0, scala.Tuple2, true]._2 AS value#304, newInstance(class scala.Tuple2), input[0, int, false] AS value#296, IntegerType, false, 0, 0)], output=[value#301, ReduceAggregator(int)#309])
+- Exchange hashpartitioning(value#301, 200)
   +- ObjectHashAggregate(keys=[value#301], functions=[partial_reduceaggregator(org.apache.spark.sql.expressions.ReduceAggregator@1d490b2b, Some(value#298), Some(int), Some(StructType(StructField(value,IntegerType,false))), input[0, scala.Tuple2, true]._1 AS value#303, input[0, scala.Tuple2, true]._2 AS value#304, newInstance(class scala.Tuple2), input[0, int, false] AS value#296, IntegerType, false, 0, 0)], output=[value#301, buf#383])
      +- AppendColumnsWithObject <function1>, [input[0, int, false] AS value#298], [input[0, int, false] AS value#301]
         +- Scan ExternalRDDScan[obj#297]
```

后来意识到，可以将DataFrames视为这些Dataset的特例，并且将API统一（使用称为[Row](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Row)的特殊优化类作为DataFrame的数据类型）。

但是，在数据集方面要牢记一个警告。作为开发人员熟悉了采集样RDD API，数据集API提供的最常用的方法自己的变种- [`filter`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset@filter(func:T=>Boolean):org.apache.spark.sql.Dataset[T])，[`map`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset@map[U](func:T=>U)(implicitevidence$6:org.apache.spark.sql.Encoder[U]):org.apache.spark.sql.Dataset[U])和[`reduce`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset@reduce(func:(T,T)=>T))。这些工作（可以预期）具有任意功能。因此，Spark无法理解此类功能的详细信息，并且由于无法再正确传播某些信息（例如，用于谓词下推），其优化能力也有所削弱。这将在序列化部分中进一步说明。

```scala
val input = spark.read.parquet("file:///tmp/test_data")
val dataframe = input.select('key).where('key === 1)
val dataset = input.as[(Int, Int)].map(_._1).filter(_ == 1)
```

**解析的逻辑计划（DataFrame）：**

```
'Filter ('key = 1)
+- Project [key#43]
   +- Relation[key#43,value#44] parquet
```

**解析的逻辑计划（DataSet）：**

```
'TypedFilter <function1>, int, [StructField(value,IntegerType,false)], unresolveddeserializer(upcast(getcolumnbyordinal(0, IntegerType), IntegerType, - root class: "scala.Int"))
+- SerializeFromObject [input[0, int, false] AS value#57]
   +- MapElements <function1>, class scala.Tuple2, [StructField(_1,IntegerType,false), StructField(_2,IntegerType,false)], obj#56: int
      +- DeserializeToObject newInstance(class scala.Tuple2), obj#55: scala.Tuple2
         +- Relation[key#43,value#44] parquet
```

**物理计划（DataFrame）：**

```
*Project [key#43]
+- *Filter (isnotnull(key#43) && (key#43 = 1))
   +- *FileScan parquet [key#43] Batched: true, Format: Parquet, Location: InMemoryFileIndex[file:/tmp/test_data], PartitionFilters: [], PushedFilters: [IsNotNull(key), EqualTo(key,1)], ReadSchema: struct<key:int>
```

**物理计划（DataSet）：**

```
*SerializeFromObject [input[0, int, false] AS value#57]
+- *Filter <function1>.apply$mcZI$sp
   +- *MapElements <function1>, obj#56: int
      +- *DeserializeToObject newInstance(class scala.Tuple2), obj#55: scala.Tuple2
         +- *FileScan parquet [key#43,value#44] Batched: true, Format: Parquet, Location: InMemoryFileIndex[file:/tmp/test_data], PartitionFilters: [], PushedFilters: [], ReadSchema: struct<key:int,value:int>
```

### 并行转换 Parallel transformations

Spark可以并行运行多个计算。这可以通过在驱动程序上启动多个线程并在每个线程中发出一组转换来轻松实现。然后，结果任务将同时运行并共享应用程序的资源。这样可以确保资源永远不会保持空闲状态（例如，在等待特定转换的最后任务完成时）。默认情况下，任务以FIFO方式（在作业级别）进行处理，但是可以通过使用备用[应用程序内调度程序](https://spark.apache.org/docs/latest/job-scheduling.html#scheduling-within-an-application)来确保公平（通过将设置`spark.scheduler.mode`为`FAIR`）来更改此任务。然后，希望线程通过将`spark.scheduler.pool`local属性（使用`SparkContext.setLocalProperty`）设置为适当的池名称来设置其调度池。然后，应在`spark.scheduler.allocation.file`设置定义的[XML文件](https://spark.apache.org/docs/latest/job-scheduling.html#configuring-pool-properties)（默认情况下，此`fairscheduler.xml`文件位于Spark的conf文件夹中）。

```scala
def input(i: Int) = sc.parallelize(1 to i*100000)
def serial = (1 to 10).map(i => input(i).reduce(_ + _)).reduce(_ + _)
def parallel = (1 to 10).map(i => Future(input(i).reduce(_ + _))).map(Await.result(_, 10.minutes)).reduce(_ + _)
```

| 计算方式 | 平均时间 | Min时间 | Max时间 |
| :------- | -------: | ------: | ------: |
| 串行     |  173.1ms |   140ms |   336ms |
| 平行     |    141ms |   122ms |   200ms |

## 2.分区 Partitioning

大多数Spark作业遭受的第二个问题是数据分区不足。为了使我们的计算高效，重要的是将我们的数据划分为足够多的分区，这些分区的大小应尽可能彼此接近（统一），以便Spark可以调度正在执行的各个任务他们以不可知论的方式仍然可以预测。如果分区不统一，则说该分区是倾斜的。发生这种情况可能有多种原因，并且可能发生在我们计算的不同部分。

![分区偏斜示例](https://michalsenkyr.github.io/images/2018-01-04-spark-performance/skew.png)

从数据源读取时，我们的输入可能已经倾斜。在RDD API中，这通常是使用[`textFile`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@textFile(path:String,minPartitions:Int):org.apache.spark.rdd.RDD[String])和[`wholeTextFiles`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@wholeTextFiles(path:String,minPartitions:Int):org.apache.spark.rdd.RDD[(String,String)])方法完成的，它们具有令人惊讶的不同分区行为。该[`textFile`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@textFile(path:String,minPartitions:Int):org.apache.spark.rdd.RDD[String])方法旨在从（通常是较大的）文件中读取文本的每一行，默认情况下将每个输入文件块作为单独的分区加载。它还提供了一个`minPartitions`参数，当该参数大于块数时，将尝试进一步拆分这些分区以满足指定值。另一方面，[`wholeTextFiles`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@wholeTextFiles(path:String,minPartitions:Int):org.apache.spark.rdd.RDD[(String,String)])该方法用于读取（通常是较小的）文件的全部内容，将相关文件的块根据其在群集中的实际位置合并到池中，并且默认情况下为每个这些池创建一个分区（有关更多信息，请参见Hadoop的[CombineFileInputFormat](http://hadoop.apache.org/docs/current/api/org/apache/hadoop/mapreduce/lib/input/CombineFileInputFormat.html)（在其实现中使用）。`minPartitions`在这种情况下，该参数控制这些池的最大大小（等于`totalSize/minPartitions`）。所有`minPartitions`参数的默认值为2。这意味着，[`wholeTextFiles`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@wholeTextFiles(path:String,minPartitions:Int):org.apache.spark.rdd.RDD[(String,String)])如果不使用默认设置而不在群集上显式管理数据局部性，则使用非常少的分区就容易得多。用于数据读入RDDS其它方法包括其它格式，例如[`sequenceFile`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@sequenceFile[K,V](path:String,minPartitions:Int)(implicitkm:scala.reflect.ClassTag[K],implicitvm:scala.reflect.ClassTag[V],implicitkcf:()=>org.apache.spark.WritableConverter[K],implicitvcf:()=>org.apache.spark.WritableConverter[V]):org.apache.spark.rdd.RDD[(K,V)])，[`binaryFiles`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@binaryFiles(path:String,minPartitions:Int):org.apache.spark.rdd.RDD[(String,org.apache.spark.input.PortableDataStream)])和[`binaryRecords`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@binaryRecords(path:String,recordLength:Int,conf:org.apache.hadoop.conf.Configuration):org.apache.spark.rdd.RDD[Array[Byte]])，以及通用的方法[`hadoopRDD`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@hadoopRDD[K,V](conf:org.apache.hadoop.mapred.JobConf,inputFormatClass:Class[_<:org.apache.hadoop.mapred.InputFormat[K,V]],keyClass:Class[K],valueClass:Class[V],minPartitions:Int):org.apache.spark.rdd.RDD[(K,V)])以及[`newAPIHadoopRDD`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@newAPIHadoopRDD[K,V,F<:org.apache.hadoop.mapreduce.InputFormat[K,V]](conf:org.apache.hadoop.conf.Configuration,fClass:Class[F],kClass:Class[K],vClass:Class[V]):org.apache.spark.rdd.RDD[(K,V)])采用自定义格式的实现（允许自定义分区）。

分区特性经常在随机边界上变化。因此，暗示随机播放的操作将提供一个`numPartitions`指定新分区计数的参数（默认情况下，分区计数与原始RDD中的计数相同）。还可以通过改组引入偏斜，尤其是在加入数据集时。

```scala
val input = sc.parallelize(1 to 1000, 42).keyBy(Math.min(_, 10))
val joined = input.cogroup(input)
```

![连接分区大小](https://michalsenkyr.github.io/images/2018-01-04-spark-performance/join-partitions.png)

由于这些情况下的分区完全取决于所选键（特别是其[Murmur3哈希值](https://en.wikipedia.org/wiki/MurmurHash)），因此必须注意避免为通用键创建异常大的分区（例如，空键是常见的特殊情况）。一个有效的解决方案是分离相关记录，在它们的键中添加一个salt（随机值），并在多个阶段对其执行后续操作（例如reduce），以获得正确的结果。

```scala
val input1 = sc.parallelize(1 to 1000, 42).keyBy(Math.min(_, 10) + Random.nextInt(100) * 100)
val input2 = sc.parallelize(1 to 1000, 42).keyBy(Math.min(_, 10) + Random.nextInt(100) * 100)
val joined = input1.cogroup(input2)
```

![盐腌的连接分区大小](https://michalsenkyr.github.io/images/2018-01-04-spark-performance/join-partitions-salt.png)

有时甚至有更好的解决方案，例如如果其中一个数据集足够小，则使用Map侧联接。

```scala
val input = sc.parallelize(1 to 1000000, 42)
val lookup = Map(0 -> "a", 1 -> "b", 2 -> "c")
val joined = input.map(x => x -> lookup(x % 3))
```

### DataFrames and Datasets

高级API共享一种特殊的数据分区方法。将输入文件的所有数据块都添加到公用池中，就像在中一样[`wholeTextFiles`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.SparkContext@wholeTextFiles(path:String,minPartitions:Int):org.apache.spark.rdd.RDD[(String,String)])，但是然后根据两个[设置](https://spark.apache.org/docs/latest/sql-programming-guide.html#other-configuration-options)将池划分为分区：`spark.sql.files.maxPartitionBytes`，它指定最大分区大小（默认为128MB），而`spark.sql.files.openCostInBytes`，则指定估算成本打开一个可能已读取的新文件（以字节为单位）（默认为4MB）。该框架将根据此信息自动找出输入数据的最佳分区。

当涉及到对shuffle进行分区时，令人遗憾的是，缺少高级API（至少从Spark 2.2起）。通过指定`spark.sql.shuffle.partitions`设置（默认为200），只能在作业级别上静态指定分区数。

高级API可以自动将联接操作转换为广播联接。这由控制`spark.sql.autoBroadcastJoinThreshold`，它指定要广播的表的最大大小（默认为10MB）`spark.sql.broadcastTimeout`，并且控制执行者等待广播表的时间（默认为5分钟）。

### 重新分区

所有的API还提供了两种方法来控制分区的数量。第一个是[`repartition`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.rdd.RDD@repartition(numPartitions:Int)(implicitord:Ordering[T]):org.apache.spark.rdd.RDD[T])强制改组以便在指定数量的分区之间重新分配数据（通过前述的Murmur哈希）。由于混排数据是一项昂贵的操作，因此，如果可能，应避免重新分区。此操作还有更多特定的变体：可排序对RDD具有[`repartitionAndSortWithinPartitions`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.rdd.OrderedRDDFunctions@repartitionAndSortWithinPartitions(partitioner:org.apache.spark.Partitioner):org.apache.spark.rdd.RDD[(K,V)])可与自定义分区程序一起使用的功能，而DataFrame和Dataset具有[`repartition`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset@repartition(partitionExprs:org.apache.spark.sql.Column*):org.apache.spark.sql.Dataset[T])带有列参数的功能来控制分区特性。

所有API提供的第二种方法的[`coalesce`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.rdd.RDD@coalesce(numPartitions:Int,shuffle:Boolean,partitionCoalescer:Option[org.apache.spark.rdd.PartitionCoalescer])(implicitord:Ordering[T]):org.apache.spark.rdd.RDD[T])性能要比[`repartition`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.rdd.RDD@repartition(numPartitions:Int)(implicitord:Ordering[T]):org.apache.spark.rdd.RDD[T])它好得多，因为它不会shuffle数据，而只是指示Spark读取多个现有分区。但是，这只能用于减少分区数，而不能用于更改分区特性。通常没有理由使用它，因为Spark旨在利用大量的小分区，而不是减少输出中的文件数或与之一起使用时的批处理数[`foreachPartition`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.rdd.RDD@foreachPartition(f:Iterator[T]=>Unit):Unit)（例如，将结果发送到数据库） 。

## 3.序列化

正确处理的另一件棘手的事情是序列化，它有两种形式：数据序列化和闭包序列化。数据序列化是指对存储在RDD中的实际数据进行编码的过程，而闭包序列化是指与在外部引入计算（例如共享字段或变量）的数据相同的过程。区分这两个很重要，因为它们在Spark中的工作方式非常不同。

### 数据序列化

Spark支持[两种不同的序列化器](https://spark.apache.org/docs/latest/tuning.html#data-serialization)以进行数据序列化。缺省的是Java序列化，尽管它非常易于使用（仅通过实现`Serializable`接口），但效率很低。因此，建议将大多数生产用途切换到第二个受支持的Serializer [Kryo](https://github.com/EsotericSoftware/kryo)。设置`spark.serializer`为即可完成此操作`org.apache.spark.serializer.KryoSerializer`。Kryo效率更高，并且不需要实现类`Serializable`（因为它们由Kryo的[FieldSerializer](https://github.com/EsotericSoftware/kryo#fieldserializer)序列化默认）。但是，在极少数情况下，Kryo可能无法序列化某些类，这是为什么它仍不是Spark的默认值的唯一原因。注册所有预期要序列化的类也是一个好主意（Kryo将能够使用索引而不是完整的类名来标识数据类型，从而减少序列化数据的大小，从而进一步提高性能）。

```scala
case class Test(a: Int = Random.nextInt(1000000),
                b: Double = Random.nextDouble,
                c: String = Random.nextString(1000),
                d: Seq[Int] = (1 to 100).map(_ => Random.nextInt(1000000))) extends Serializable

val input = sc.parallelize(1 to 1000000, 42).map(_ => Test()).persist(DISK_ONLY)
input.count() // Force initialization
val shuffled = input.repartition(43).count()
```

| RDD  |  平均时间 | Min时间 | Max时间 |
| :--- | --------: | ------: | ------: |
| java | 65990.9ms | 64482ms | 68148ms |
| kryo | 30196.5ms | 28322ms | 33012ms |

**Lineage （Java）：**

```
(42) MapPartitionsRDD[1] at map at <console>:25 [Disk Serialized 1x Replicated]
 |        CachedPartitions: 42; MemorySize: 0.0 B; ExternalBlockStoreSize: 0.0 B; DiskSize: 3.8 GB
 |   ParallelCollectionRDD[0] at parallelize at <console>:25 [Disk Serialized 1x Replicated]
```

**Lineage ：**

```
(42) MapPartitionsRDD[1] at map at <console>:25 [Disk Serialized 1x Replicated]
 |        CachedPartitions: 42; MemorySize: 0.0 B; ExternalBlockStoreSize: 0.0 B; DiskSize: 3.1 GB
 |   ParallelCollectionRDD[0] at parallelize at <console>:25 [Disk Serialized 1x Replicated]
```

### DataFrames and Datasets

当涉及到数据序列化时，高级API效率更高，因为它们知道正在使用的实际数据类型。因此，它们可以生成专门针对这些类型以及Spark在整个计算环境中使用它们的方式量身定制的优化序列化代码。对于某些转换，它也可能仅生成部分序列化代码（例如，计数或数组查找）。此代码生成步骤是Tungsten项目的组成部分，这是使高级API如此有效的重要原因。

值得注意的是，在此过程中，Spark可以从了解所应用转换的属性中受益，因为它可以在整个作业图中传播有关正在使用哪些列的信息（谓词下推）。在转换中使用不透明函数（例如，数据集[`map`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset@map[U](func:T=>U)(implicitevidence$6:org.apache.spark.sql.Encoder[U]):org.apache.spark.sql.Dataset[U])或[`filter`](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.Dataset@filter(func:T=>Boolean):org.apache.spark.sql.Dataset[T])）时，此信息会丢失。

```scala
val input = sc.parallelize(1 to 1000000, 42).map(_ => Test()).toDS.persist(org.apache.spark.storage.StorageLevel.DISK_ONLY)
input.count() // Force initialization
val shuffled = input.repartition(43).count()
```

| 数据框   | 平均时间 | Min时间 | Max时间 |
| :------- | -------: | ------: | ------: |
| tungsten | 1102.9ms |   912ms |  1776ms |

**Lineage ：**

```
(42) MapPartitionsRDD[13] at rdd at <console>:30 []
 |   MapPartitionsRDD[12] at rdd at <console>:30 []
 |   MapPartitionsRDD[11] at rdd at <console>:30 []
 |   *SerializeFromObject [assertnotnull(input[0, $line16.$read$$iw$$iw$Test, true]).a AS a#5, assertnotnull(input[0, $line16.$read$$iw$$iw$Test, true]).b AS b#6, staticinvoke(class org.apache.spark.unsafe.types.UTF8String, StringType, fromString, assertnotnull(input[0, $line16.$read$$iw$$iw$Test, true]).c, true) AS c#7, newInstance(class org.apache.spark.sql.catalyst.util.GenericArrayData) AS d#8]
+- Scan ExternalRDDScan[obj#4]
 MapPartitionsRDD[4] at persist at <console>:27 []
 |       CachedPartitions: 42; MemorySize: 0.0 B; ExternalBlockStoreSize: 0.0 B; DiskSize: 3.2 GB
 |   MapPartitionsRDD[3] at persist at <console>:27 []
 |   MapPartitionsRDD[2] at persist at <console>:27 []
 |   MapPartitionsRDD[1] at map at <console>:27 []
 |   ParallelCollectionRDD[0] at parallelize at <console>:27 []
```

### 闭包序列化

在大多数Spark应用程序中，不仅需要序列化数据本身。在各个转换中还使用了外部字段和变量。让我们考虑以下代码片段：

```scala
val factor = config.multiplicationFactor
rdd.map(_ * factor)
```

在这里，我们使用从应用程序配置中加载的值作为计算本身的一部分。但是，由于转换函数之外发生的所有事情都发生在驱动程序上，因此Spark必须将值传输给相关的执行程序。因此，Spark在其中计算函数的[闭包](https://spark.apache.org/docs/latest/rdd-programming-guide.html#understanding-closures-a-nameclosureslinka)`map`由它使用的所有外部值组成，将这些值序列化并通过网络发送。由于闭包可能非常复杂，因此决定只支持Java序列化。因此，闭包的序列化不如数据本身的序列化有效，但是，由于闭包仅针对每个转换的每个执行者而不是每个记录进行序列化，因此通常不会引起性能问题。（但是，实现这些值会有不愉快的副作用`Serializable`。）

闭包中的变量很容易跟踪。使用字段可能会造成很多混乱。让我们看下面的例子：

```scala
class SomeClass(d: Int) extends Serializable {
  val c = 1
  val e = new SomeComplexClass

  def closure(rdd: RDD[Int], b: Int): RDD[Int] = {
    val a = 0
    rdd.map(_ + a + b + c + d)
  }
}
```

在这里，我们可以看到它`a`只是一个变量（与`factor`以前一样），因此被序列化为`Int`。`b`是一个方法参数（也表现为变量），因此也被序列化为`Int`。但是`c`是一个类字段，因此不能单独序列化。这意味着为了序列化它，Spark需要`SomeClass`使用它序列化它的整个实例（因此它必须扩展`Serializable`，否则我们将得到一个运行时异常）。对于`d`内部将构造函数参数转换为字段的情况也是如此。因此，在这两种情况下，Spark也必须发送的值`c`，`d`并`e`给Executors。如`e`序列化可能会非常昂贵，这绝对不是一个好的解决方案。我们可以通过避免闭包中的类字段来解决此问题：

```
class SomeClass(d: Int) {
  val c = 1
  val e = new SomeComplexClass

  def closure(rdd: RDD[Int], b: Int): RDD[Int] = {
    val a = 0
    val sum = a + b + c + d
    rdd.map(_ + sum)
  }
}
```

在这里，我们通过将值存储在局部变量中来准备值`sum`。然后将其序列化为一个简单的对象，`Int`而不会拖动它的整个实例`SomeClass`（因此它不再需要扩展`Serializable`）。

Spark还定义了一种特殊的构造，以在需要为多个转换序列化相同值的情况下提高性能。它被称为[广播变量](https://spark.apache.org/docs/latest/rdd-programming-guide.html#broadcast-variables)，在计算之前被序列化并仅发送一次给所有执行者。这对于诸如查找表之类的[大变量](https://spark.apache.org/docs/latest/tuning.html#broadcasting-large-variables)特别有用。

```scala
val broadcastMap = sc.broadcast(Map(0 -> "a", 1 -> "b", 2 -> "c"))
val input = sc.parallelize(1 to 1000000, 42)
val joined = input.map(x => x -> broadcastMap.value(x % 3))
```

Spark提供了一个有用的工具来确定内存中对象的实际大小，称为[SizeEstimator](https://spark.apache.org/docs/latest/api/java/index.html?org/apache/spark/util/SizeEstimator.html)，它可以帮助我们确定特定对象是否适合广播变量。

## 4.内存管理 Memory management

对于应用程序而言，重要的是要有效地使用其内存空间。由于每个应用程序的内存要求不同，Spark将应用程序的驱动程序和执行程序的内存划分为多个部分，这些部分由适当的规则控制，并通过应用程序设置将大小大小留给用户。

### 驱动程序内存

![Spark驱动程序内存图](https://michalsenkyr.github.io/images/2018-01-04-spark-performance/spark-driver-memory.svg)

驱动程序的内存结构非常简单。它仅使用其所有已配置的内存（由`spark.driver.memory`设置控制，默认为1GB）作为共享堆空间。在群集部署设置中，还增加了开销，以防止YARN因使用过多资源而过早地终止驱动程序容器。

### 执行器内存

![Spark执行器内存图](https://michalsenkyr.github.io/images/2018-01-04-spark-performance/spark-executor-memory.svg)

执行程序需要将其[内存](https://spark.apache.org/docs/latest/tuning.html#memory-management-overview)用于一些主要目的：用于当前转换的中间数据（执行内存），用于缓存的持久性数据（存储内存）以及用于转换的自定义数据结构（用户内存）。由于Spark可以计算每个存储记录的实际大小，因此它可以监视执行和存储部分并做出相应的反应。执行内存的大小通常非常不稳定，需要立即使用，而存储内存的寿命更长，稳定，通常可以逐出磁盘，而应用程序通常只需要整个计算的某些部分（有时根本不需要） ）。因此，Spark为两者定义了一个共享空间，从而优先考虑执行内存。所有这些都由几个设置控制：`spark.executor.memory`（默认为1GB）定义了可用堆空间的总大小，`spark.memory.fraction`设置（默认为0.6）定义了执行和存储共享的内存的一部分（减去300MB缓冲区），并且`spark.memory.storageFraction`（默认值为0.5）定义了无法执行的存储部分。以最适合您的应用程序的方式定义它们很有用。例如，如果应用程序大量使用缓存的数据并且不使用过多的聚合，则可以增加存储内存的比例以容纳将所有缓存的数据存储在RAM中，从而加快数据的读取速度。另一方面，如果应用程序使用昂贵的聚合并且不严重依赖缓存，则增加执行内存可以通过逐出不需要的缓存数据来改善计算本身，从而有所帮助。此外，请记住，您的自定义对象必须适合用户内存。

Spark还可以将堆外内存用于存储和部分执行，这由设置`spark.memory.offHeap.enabled`（默认为false），`spark.memory.offHeap.size`（默认为0）和`OFF_HEAP`持久性级别控制。这样可以减轻垃圾收集的暂停。

### DataFrames and Datasets

作为Tungsten项目的一部分，高级API使用自己的方式来管理内存。由于数据类型是框架已知的，并且它们的生命周期定义非常明确，因此可以通过预先分配内存块并显式微管理这些块来完全避免垃圾回收。这样可以极大地重用已分配的内存，从而有效地消除了对执行内存进行垃圾回收的需要。这种优化实际上效果很好，以至于启用堆外内存几乎没有其他好处（尽管仍有很多好处）。

## 5.集群资源 Cluster resources

导致性能降低的最后一个重要点是群集资源分配不足。从低效率地使用数据局部性（通过与散乱的执行程序打交道）到防止在不需要集群资源时浪费集群资源，这种形式有很多种。

### 数据局部性

为了获得良好的性能，我们的应用程序的计算应[尽可能接近实际数据](https://spark.apache.org/docs/latest/tuning.html#data-locality)，以避免不必要的传输。这意味着在存储数据本身的计算机上运行执行程序是一个非常好的主意。使用HDFS时，Spark可以以最大程度地提高这种可能性来优化执行程序的分配。但是，我们可以通过良好的设计来进一步提高这一点。

通过增加单个执行程序的资源，同时减少执行程序的总数，我们可以减少所需的节点间通信量，从本质上迫使任务必须由数量有限的节点来处理。以以下示例资源分配为例：

| num_executors | executor_cores | executor_memory |
| ------------: | -------------: | --------------: |
|            15 |              1 |              1g |
|             5 |              3 |              3g |
|             3 |              5 |              5g |

在所有情况下，我们将使用相同数量的资源（15个内核和15GB内存）。但是，由于我们减少了执行程序的总数，因此也减少了在执行程序之间传输数据的需求。通常使第三个选项最快。另一方面，取决于请求的操作，节点级别的I / O吞吐量可能会受到限制，因此我们不能无限地增加它。例如，对于HDFS I / O，每个执行者的核心数量被认为可以达到大约五个峰值。

当使用`spark.locality.wait`设置（默认为3秒）及其子部分（`spark.locality.wait`默认情况下相同）从集群中读取数据时，我们还可以调整Spark与局部性相关的配置。这些定义了基于位置的计划的超时（达到时降低了位置限制）。

### 动态分配

在应用程序范围内对执行程序进行明确的分配可能会有其不利之处。在某些情况下，我们可能不希望在整个计算期间都拥有统一数量的执行程序，而是想要一些扩展。在给定的时间群集上可能没有足够的资源，但是无论如何，我们都希望运行计算，我们可能正在处理一个需要更少资源并且不希望消耗更多资源的转换，依此类推。其中，[动态分配](https://spark.apache.org/docs/latest/job-scheduling.html#dynamic-resource-allocation)的用武之地。

使用动态分配（通过设置`spark.dynamicAllocation.enabled`为true 启用），Spark通过尝试分配尽可能多的执行程序来开始每个阶段（最多达到给定阶段的最大并行度`spark.dynamicAllocation.maxExecutors`，默认情况下为infinity），其中第一阶段必须至少获得`spark.dynamicAllocation.initialExecutors`（与`spark.dynamicAllocation.minExecutors`或`spark.executor.instances`默认情况下）。

在计算过程中，如果执行程序空闲时间超过`spark.dynamicAllocation.executorIdleTimeout`了默认时间（默认情况下为60秒），它将被删除（除非它将执行程序的数量降至以下值`spark.dynamicAllocation.minExecutors`（默认情况下为0）。这确保了我们的应用程序在执行时不会不必要地占用集群资源更便宜的改造。

为了能够启用动态分配，我们还必须启用Spark的外部随机播放服务。它充当在群集中每台计算机上运行的独立服务器，当适当的执行程序不再存在（已被删除或丢失）时，它能够管理随机播放文件。这在遗失执行者（例如由于抢占）的情况下也是有益的，因为所讨论的随机数据不必重新计算。

### 投机执行

有时，即使我们正确地进行了所有操作，由于我们无法控制的情况（与Spark，硬件故障等无关的高负载），我们仍然可能在特定计算机上获得较差的性能。对于这些情况，我们可能会指示Spark在检测到此类散乱者后自动重新执行任务。为此，启用`spark.speculation`设置。可以使用以下设置配置检测例程：`spark.speculation.interval`定义检查散乱者的频率（默认为100ms），`spark.speculation.multiplier`定义散乱者的速度必须慢多少倍（默认为1.5）并`spark.speculation.quantile`定义必须执行的任务比例直到检测程序开始运行（默认为0.75）。

## 结论

如您所见，为性能而设计一个Spark应用程序可能会非常具有挑战性，并且此过程的每一步似乎都在增加复杂性，降低多功能性或延长对特定用例的分析方面付出了代价。幸运的是，由于典型的Spark应用程序对性能并不敏感，因此几乎不需要全部实现。此外，仅通过使用高级API（DataFrames或DataSets）就可以实现很多目标。尽管必须在开发过程的早期就做出使用它们的决定，因为切换它们并非易事。

此外，还有许多其他技术可以帮助进一步提高Spark作业的性能。即[GC调整](https://spark.apache.org/docs/latest/tuning.html#garbage-collection-tuning)，适当的[硬件配置](https://spark.apache.org/docs/latest/hardware-provisioning.html#hardware-provisioning)和调整Spark的众多[配置选项](https://spark.apache.org/docs/latest/configuration.html)。

