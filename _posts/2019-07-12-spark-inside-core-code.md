---
typora-root-url: ../
analytics: true
comments: true
title: Spark内核源码深度剖析
categories: "technology"
tags:
  - spark
  - bigdata
---

Spark内核源码深度剖析

---

## Spark内核架构深度剖析

![](http://i2.51cto.com/images/blog/201810/03/6c61cff671e7c5ba2a78285031c5a139.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)




 Spark内核架构


    1、Application
    2、spark-submit
    3、Driver
    4、SparkContext
    5、Master
    6、Worker
    7、Executor
    8、Job
    9、DAGScheduler
    10、TaskScheduler
    11、ShuffleMapTask and ResultTask



## 宽依赖与窄依赖深度剖析


![](http://i2.51cto.com/images/blog/201810/03/3277925bde5daab63c000925f86e200c.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

## 基于Yarn的两种提交模式深度剖析


 Spark的三种提交模式


    1、Spark内核架构，其实就是第一种模式，standalone模式，基于Spark自己的Master-Worker集群。
    2、第二种，是基于YARN的yarn-cluster模式。
    3、第三种，是基于YARN的yarn-client模式。
    4、如果，你要切换到第二种和第三种模式，很简单，将我们之前用于提交spark应用程序的spark-submit脚本，
    加上--master参数，设置为yarn-cluster，或yarn-client，即可。如果你没设置，那么，就是standalone模式。


基于YARN的两种提交模式深度剖析：


![](http://i2.51cto.com/images/blog/201810/03/c1f482844f6b387c6488a15d7c9d66b7.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

```
1. SparkSubmit client (yarnClient)
org.apache.spark.deploy.SparkSubmit
  // 启动进程
  main()
    // 解析参数
    parseArguments(args)
      new SparkSubmitArguments(args)
    // 提交
    submit()
      // 准备提交环境 childMainClass = "org.apache.spark.deploy.yarn.YarnClusterApplication"
      val (childArgs, childClasspath, sparkConf, childMainClass) = prepareSubmitEnvironment(args)
      doRunMain()
        runMain()
          // 反射加载类
          mainClass = Utils.classForName(childMainClass)
          // 构造SparkApplication app
          app.start(childArgs.toArray, sparkConf)
            // 若app是org.apache.spark.deploy.yarn.YarnClusterApplication
            new Client(new ClientArguments(args), conf)
              val yarnClient = YarnClient.createYarnClient
            new Client(new ClientArguments(args), conf).run()
              this.appId = submitApplication()
                yarnClient.init(hadoopConf)
                yarnClient.start()
                // 封装命令 command = bin/java "org.apache.spark.deploy.yarn.ApplicationMaster" (cluster)
                // command = bin/java "org.apache.spark.deploy.yarn.ExecutorLauncher" (client)
                val containerContext = createContainerLaunchContext(newAppResponse)
                val appContext = createApplicationSubmissionContext(newApp, containerContext)
                yarnClient.submitApplication(appContext)
                rmClient.submitApplication(request);
                  rmAppManager.submitApplication(submissionContext, System.currentTimeMillis(), user);
                    RMAppImpl application = createAndPopulateNewRMApp(submissionContext, submitTime, user, false);


2. Driver
org.apache.spark.deploy.yarn.ApplicationMaster
  main()
    val amArgs = new ApplicationMasterArguments(args)
    master = new ApplicationMaster(amArgs)
    master.run()
      runImpl()
        // cluster
        runDriver()
          // 启动用户应用
          userClassThread = startUserApplication()
            // 获取用户应用类的main方法
            val mainMethod = userClassLoader.loadClass(args.userClass).getMethod("main", classOf[Array[String]])
            // Thread运行mainMethod.invoke(null, userArgs.toArray)
            new Thread().start()
          registerAM(host, port, userConf, sc.ui.map(_.webUrl))
          createAllocator(driverRef, userConf)
            allocator = client.createAllocator(...)
          resumeDriver()

3. CoarseGrainedExecutorBackend
org.apache.spark.executor.CoarseGrainedExecutorBackend
  main()
    run()
      onStart()
        ref.ask[Boolean](RegisterExecutor(executorId, self, hostname, cores, extractLogUrls))
      receive()
        // case RegisteredExecutor
        executor = new Executor(executorId, hostname, env, userClassPath, isLocal = false)
        // LaunchTask(data)
        executor.launchTask(this, taskDesc)
```





## SparkContext原理剖析与源码分析


 SparkContex原理剖析

    1、TaskScheduler
    2、DAGScheduler
    3、SparkUI

![](http://i2.51cto.com/images/blog/201810/03/74d7cbe8d9037580734f134210e747b0.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)


## Master主备切换机制原理剖析与源码分析

 Master原理剖析与源码分析

    1、主备切换机制原理剖析与源码分析


​    


主备切换机制原理剖析：

![](http://i2.51cto.com/images/blog/201810/03/3dc4010b9f6b0c6b37c27f4adfc8a02d.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)



## Master注册机制原理剖析与源码分析

    2、注册机制原理剖析与源码分析


​    
注册机制原理剖析：


![](http://i2.51cto.com/images/blog/201810/03/c5e771f04be1cd7061e4bc6b1770991a.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)



## Master状态改变处理机制原理剖析与源码分析

    3、状态改变处理机制源码分析


## Master资源调度算法原理剖析与源码分析

    4、资源调度机制源码分析（schedule()，两种资源调度算法）


## Worker原理剖析与源码分析

Worker原理剖析：

![](http://i2.51cto.com/images/blog/201810/03/b590969fdc3927e4bc18c9f1ddc98aa0.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)



## job触发流程原理剖析与源码分析


 wordcount


    val lines = sc.textFile()
    val words = lines.flatMap(line => line.split(" "))
    val pairs = words.map(word => (word, 1))

 其实RDD里是没有reduceByKey的，因此对RDD调用reduceByKey()方法的时候，会触发scala的隐式转换；此时就会在作用域内，寻找隐式转换，会在RDD中找到rddToPairRDDFunctions()隐式转换，然后将RDD转换为PairRDDFunctions。

 接着会调用PairRDDFunctions中的reduceByKey()方法

    val counts = pairs.reduceByKey(_ + _)
    
    counts.foreach(count => println(count._1 + ": " + count._2))


## DAGScheduler原理剖析与源码分析

stage划分算法原理剖析：

![](http://i2.51cto.com/images/blog/201810/03/3a6416e270ca0bdab5f85091e1a0bbda.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)



## TaskScheduler原理剖析与源码分析

## Executor原理剖析与源码分析


 Executor原理剖析与源码分析

    1、CoarseGrainedExecutorBackend
    2、Executor注册机制
    3、启动task机制

Executor原理剖析：

![](http://i2.51cto.com/images/blog/201810/03/8b81198b0ceb8b3de7e828ca77deec40.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)


## Task原理剖析与源码分析

Task原理剖析：

![](http://i2.51cto.com/images/blog/201810/03/897819700ae1f0a02eae70b993a9d8a5.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)


## Shuffle原理剖析与源码分析

###  Shuffle原理剖析与源码分析


​    
​    1、在Spark中，什么情况下，会发生shuffle？reduceByKey、groupByKey、sortByKey、countByKey、join、cogroup等操作。
​    2、默认的Shuffle操作的原理剖析
​    3、优化后的Shuffle操作的原理剖析
​    4、Shuffle相关源码分析



###  Spark Shuffle操作的两个特点


### 第一个特点，

在Spark早期版本中，那个bucket缓存是非常非常重要的，因为需要将一个ShuffleMapTask所有的数据都写入内存缓存之后，才会刷新到磁盘。但是这就有一个问题，如果map side数据过多，那么很容易造成内存溢出。所以spark在新版本中，优化了，默认那个内存缓存是100kb，然后呢，写入一点数据达到了刷新到磁盘的阈值之后，就会将数据一点一点地刷新到磁盘。

这种操作的优点，是不容易发生内存溢出。缺点在于，如果内存缓存过小的话，那么可能发生过多的磁盘写io操作。所以，这里的内存缓存大小，是可以根据实际的业务情况进行优化的。

### 第二个特点，

与MapReduce完全不一样的是，MapReduce它必须将所有的数据都写入本地磁盘文件以后，才能启动reduce操作，来拉取数据。为什么？因为mapreduce要实现默认的根据key的排序！所以要排序，肯定得写完所有数据，才能排序，然后reduce来拉取。

但是Spark不需要，spark默认情况下，是不会对数据进行排序的。因此ShuffleMapTask每写入一点数据，ResultTask就可以拉取一点数据，然后在本地执行我们定义的聚合函数和算子，进行计算。

spark这种机制的好处在于，速度比mapreduce快多了。但是也有一个问题，mapreduce提供的reduce，是可以处理每个key对应的value上的，很方便。但是spark中，由于这种实时拉取的机制，因此提供不了，直接处理key对应的values的算子，只能通过groupByKey，先shuffle，有一个MapPartitionsRDD，然后用map算子，来处理每个key对应的values。就没有mapreduce的计算模型那么方便。


## BlockManager原理剖析与源码分析

BlockManager原理剖析：

![](http://i2.51cto.com/images/blog/201810/03/889fba8a70502281ba3ab060e640d80e.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)


## CacheManager原理剖析与源码分析

CacheManager原理剖析：

![](http://i2.51cto.com/images/blog/201810/03/206e795a39f9370bbaf136b39e3ad144.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

## Checkpoint原理剖析

###  Checkpoint是什么？

Checkpoint，是Spark提供的一个比较高级的功能。有的时候啊，比如说，我们的Spark应用程序，特别的复杂，然后呢，从初始的RDD开始，到最后整个应用程序完成，有非常多的步骤，比如超过20个transformation操作。而且呢，整个应用运行的时间也特别长，比如通常要运行1~5个小时。

在上述情况下，就比较适合使用checkpoint功能。因为，对于特别复杂的Spark应用，有很高的风险，会出现某个要反复使用的RDD，因为节点的故障，虽然之前持久化过，但是还是导致数据丢失了。那么也就是说，出现失败的时候，没有容错机制，所以当后面的transformation操作，又要使用到该RDD时，就会发现数据丢失了（CacheManager），此时如果没有进行容错处理的话，那么可能就又要重新计算一次数据。

简而言之，针对上述情况，整个Spark应用程序的容错性很差。




###  Checkpoint的功能



所以，针对上述的复杂Spark应用的问题（没有容错机制的问题）。就可以使用checkponit功能。

checkpoint功能是什么意思？checkpoint就是说，对于一个复杂的RDD chain，我们如果担心中间某些关键的，在后面会反复几次使用的RDD，可能会因为节点的故障，导致持久化数据的丢失，那么就可以针对该RDD格外启动checkpoint机制，实现容错和高可用。

checkpoint，就是说，首先呢，要调用SparkContext的setCheckpointDir()方法，设置一个容错的文件系统的目录，比如说HDFS；然后，对RDD调用调用checkpoint()方法。之后，在RDD所处的job运行结束之后，会启动一个单独的job，来将checkpoint过的RDD的数据写入之前设置的文件系统，进行高可用、容错的类持久化操作。

那么此时，即使在后面使用RDD时，它的持久化的数据，不小心丢失了，但是还是可以从它的checkpoint文件中直接读取其数据，而不需要重新计算。（CacheManager）




###  Checkpoint原理剖析

    1、如何进行checkpoint？
        SparkContext.setCheckpointDir()
        RDD.checkpoint()
    2、Checkpoint原理剖析
    3、Checkpoint与持久化的不同：lineage的改变
    4、RDD.iterator()：读取checkpoint数据
    5、给要checkpoint的RDD，先进行persist(StorageLevel.DISK_ONLY)



![](http://i2.51cto.com/images/blog/201810/03/3022304bfaed6bd2fc1cf8fe8198332c.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)













































































































