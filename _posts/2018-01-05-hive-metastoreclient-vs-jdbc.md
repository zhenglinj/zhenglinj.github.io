---
typora-root-url: ../
title: "Hive MetaStoreClient VS JDBC HiveQL"
categories: "technology"
tags:
  - hive
  - big-data
---


介绍HiveMetaStore的部署架构，以及，Hive Partition Client组件根据Hive Metastore的部署架构采用不同的库实现不同版本并简单比较，MetaStoreClient对比JDBC HiveQL

---

## Hive Metastore配置

基于CDH大数据平台配置Hive Metastore，有三种不同的部署模式。

### Embedded Mode

**Cloudera建议用于体验** 这种模式容易配置，但是同一时间只支持单用户连接并且生产也没有保障。

### Local Mode

Hive Metastore服务和Metastore数据库部署在不同的主机，用JDBC连接。

### Remote Mode

**Cloudera建议这种模式用于生产环境**

> In Remote mode, the Hive metastore service runs in its own JVM process. HiveServer2, HCatalog, Impala, and other processes communicate with it using the Thrift network API (configured using the hive.metastore.uris property). The metastore service communicates with the metastore database over JDBC (configured using the javax.jdo.option.ConnectionURL property). The database, the HiveServer process, and the metastore service can all be on the same host, but running the HiveServer process on a separate host provides better availability and scalability.
> 
> The main advantage of Remote mode over Local mode is that Remote mode does not require the administrator to share JDBC login information for the metastore database with each Hive user. HCatalog requires this mode.

具体的配置过程见Cloudera文档[Configuring the Hive Metastore](https://www.cloudera.com/documentation/enterprise/5-8-x/topics/cdh_ig_hive_metastore_configure.html)

## HiveMetaStoreClient, HiveJdbcDriver

> using hive metastore server, which then connects in the background to a relational db such as mysql for schema manifestation. This runs on port 9083, generally.
>
> using hive jdbc server, called HiveServer2, which runs on port 10001, generally
>
> Now, in the earlier editions of hive, hiveserver2 used to be not so stable and in fact it's multi-threading support was also limited. Things have probably improved in that arena, I'd imagine.
> 
> So for JDBC api - yes, it would let you communicate using JDBC and sql.
> 
> For the metastore connectivity, there appear to be 2 features.
> 
> - to actually run SQL queries - DML
> - to perform DDL operations - DDL
> 
> DDL, the metastore APIs come in handy, org.apache.hadoop.hive.metastore.HiveMetaStoreClient HiveMetaStoreClient class can be utilized for that purpose
> 
> DML, what I have found useful in this regard is the org.apache.hadoop.hive.ql.Driver https://hive.apache.org/javadocs/r0.13.1/api/ql/org/apache/hadoop/hive/ql/Driver.html hive.ql.Driver class This class has a method called run() which lets you execute a SQL statement and get the result back. for e.g. you can do following
> 
```java
Driver driver = new Driver(hiveConf);
HiveMetaStoreClient client = new HiveMetaStoreClient(hiveConf);
SessionState.start(new CliSessionState(hiveConf));
driver.run("select  * from employee");
// DDL example
client.dropTable(db, table);
```

### HiveMetaStoreClient, HiveJdbcDriver, HiveServer2



## 参考

[https://github.com/Re1tReddy/HiveMetaStoreClient](https://github.com/Re1tReddy/HiveMetaStoreClient) This Project explains how to use HiveMetaStoreClient, HiveJdbcDriver, HiveServer2

[https://stackoverflow.com/questions/33377198/connecting-to-hivemetastore-on-cluster-with-kerberos](https://stackoverflow.com/questions/33377198/connecting-to-hivemetastore-on-cluster-with-kerberos)

[https://community.hortonworks.com/questions/21993/hcatalog-and-kerberos.html](https://community.hortonworks.com/questions/21993/hcatalog-and-kerberos.html)

[https://github.com/onefoursix/Cloudera-Impala-JDBC-Example](https://github.com/onefoursix/Cloudera-Impala-JDBC-Example)

