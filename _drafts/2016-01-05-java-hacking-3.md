---
layout: post
title: "Java 之禅 高级"
description: "Java 学习笔记之高级篇"
category: "technology"
draft: false
analytics: true
comments: true
tags: [java, 笔记]
---
{% include JB/setup %}

Java 学习笔记之高级篇

---

3.1. 编译原理知识

3.1.1. 用Java实现以下表达式解析并返回结果（语法和Oracle中的select sysdate-1 from dual类似）

 sysdate
 sysdate - 1
 sysdate - 1/24
 sysdate - 1/(12*2)
3.1.2. 实现对一个List通过DSL筛选

  QList<Map<String, Object>> mapList = new QList<Map<String, Object>>;
  mapList.add({"name": "hatter test"});
  mapList.add({"id": -1,"name": "hatter test"});
  mapList.add({"id": 0, "name": "hatter test"});
  mapList.add({"id": 1, "name": "test test"});
  mapList.add({"id": 2, "name": "hatter test"});
  mapList.add({"id": 3, "name": "test hatter"});
  mapList.query("id is not null and id > 0 and name like '%hatter%'");
要求返回列表中匹配的对象，即最后两个对象；

3.1.3. 用Java实现以下程序（语法和变量作用域处理都和JavaScript类似）：

代码：

var a = 1;
var b = 2;
var c = function() {
  var a = 3;
  println(a);
  println(b);
};
c();
println(a);
println(b);
输出：

3
2
1
2
3.1.4. 参考资料

http://en.wikipedia.org/wiki/Abstract_syntax_tree https://javacc.java.net/ http://www.antlr.org/

3.2. 操作系统知识

Ubuntu Centos 使用linux，熟悉shell脚本

3.3. 数据存储知识

3.3.1. 关系型数据库

MySQL 如何看执行计划 如何搭建MySQL主备 binlog是什么 Derby，H2，PostgreSQL SQLite

3.3.2. NoSQL

Cache Redis Memcached Leveldb Bigtable HBase Cassandra Mongodb 图数据库 neo4j

3.3.3. 参考资料

http://db-engines.com/en/ranking

http://redis.io/

https://code.google.com/p/leveldb/

http://hbase.apache.org/

http://cassandra.apache.org/

http://www.mongodb.org/

http://www.neo4j.org/

3.4. 大数据知识

3.4.1. Zookeeper，在linux上部署zk

3.4.2. Solr，Lucene，ElasticSearch

在linux上部署solr，solrcloud，，新增、删除、查询索引

3.4.3. Storm，流式计算，了解Spark，S4

在linux上部署storm，用zookeeper做协调，运行storm hello world，local和remote模式运行调试storm topology。

3.4.4. Hadoop，离线计算

Hdfs：部署NameNode，SecondaryNameNode，DataNode，上传文件、打开文件、更改文件、删除文件

MapReduce：部署JobTracker，TaskTracker，编写mr job

Hive：部署hive，书写hive sql，得到结果

Presto：类hive，不过比hive快，非常值得学习

3.4.5. 分布式日志收集flume，kafka，logstash

3.4.6. 数据挖掘，mahout

3.4.7. 参考资料

http://zookeeper.apache.org/

https://lucene.apache.org/solr/

https://github.com/nathanmarz/storm/wiki

http://hadoop.apache.org/

http://prestodb.io/

http://flume.apache.org/

http://logstash.net/

http://kafka.apache.org/

http://mahout.apache.org/

3.5. 网络安全知识

3.5.1. 什么是DES、AES

3.5.2. 什么是RSA、DSA

3.5.3. 什么是MD5，SHA1

3.5.4. 什么是SSL、TLS，为什么HTTPS相对比较安全

3.5.5. 什么是中间人攻击、如果避免中间人攻击

3.5.6. 什么是DOS、DDOS、CC攻击

3.5.7. 什么是CSRF攻击

3.5.8. 什么是CSS攻击

3.5.9. 什么是SQL注入攻击

3.5.10. 什么是Hash碰撞拒绝服务攻击

3.5.11. 了解并学习下面几种增强安全的技术

http://www.openauthentication.org/

HOTP http://www.ietf.org/rfc/rfc4226.txt

TOTP http://tools.ietf.org/rfc/rfc6238.txt

OCRA http://tools.ietf.org/rfc/rfc6287.txt

http://en.wikipedia.org/wiki/Salt_(cryptography)

3.5.12. 用openssl签一个证书部署到apache或nginx

3.5.13. 参考资料

http://en.wikipedia.org/wiki/Cryptographic_hash_function

http://en.wikipedia.org/wiki/Block_cipher

http://en.wikipedia.org/wiki/Public-key_cryptography

http://en.wikipedia.org/wiki/Transport_Layer_Security

http://www.openssl.org/

https://code.google.com/p/google-authenticator/
