---
typora-root-url: ../
analytics: true
comments: true
link: http://www.google.com/
title: "title"
categories: "technology"
tags:
  - tags
---

---

## 大数据平台数据仓库小结

### 分层

#### 分层的作用

1. 清晰数据结构：每一个数据分层都有它的作用域和职责，在使用表的时候能更方便地定位和理解
2. 减少重复开发：规范数据分层，开发一些通用的中间层数据，能够减少极大的重复计算
3. 统一数据口径：通过数据分层，提供统一的数据出口，统一对外输出的数据口径
4. 复杂问题简单化：将一个复杂的任务分解成多个步骤来完成，每一层解决特定的问题



#### 层次结构

##### 数据运营层：ODS层（Operational Data Store）

用于存放贴源数据，将数据源中的数据经过轻度的ETL之后，存入本层。不建议做过多的数据清洗工作。

具体任务：
1. 统一字段命名规范
2. 统一字段类型
3. 设置默认值
4. 屏蔽数据源表信息的变化对数据仓库层的影响
5. 非结构化处理（例如json数据）

##### 数据仓库层：DW层（Data Warehouse）

这一层从ODS层获取数据，按照主题建立各种数据模型。
用于将贴源层数据，按照维度建模和星型模式架构的方式，将数据进行聚合、维度拆分，形成用于数据分析的宽表数据。

**DW层细分为：DWD层、DWM层、DWS层**

**DWD层（Data Warehouse Detail）**：该层已取消，该层的部分工作在ODS层和DWM层完成，减少开发流程提高效率。后续跟进业务需要进行调整。

**DWM层（Data WareHouse Middle）**：

存放轻度汇总数据，按照星型模型，生成事实表和不同的维表。
该层在ODS层的基础上，对数据进行维度退化处理，生成相应的事实表，维度表，临时表，提升公共指标的复用性，减少重复加工，按照不同的维度将数据聚合，生成相应的维度表
并且在该层对数据的变化信息，做拉链表处理。

具体任务：
1. 生成维度表（主要分为两种）
2. 高基数维度数据：一般是用户资料表、商品资料表类似的资料表，数据量可能是几千万上亿的级别
3. 低基数维度数据：一般是配置表，比如枚举值对应的中文含义，或者日期维表。数据量可能是个位数或几千几万
4. 生成事实表
5. 生成拉链表：记录数据的变化信息。

**DWS层（Data WareHouse Servce）**：

存放数据集市（宽表）数据。高度汇总数据。
tips：实际计算中，如果直接从DWD或ODS层计算出宽表的统计指标，会存在计算量太大并且维度较少的问题，因此一般的做法是，在DWM层先计算出多个小的中间表，然后再拼接成一张DWS的宽表，由于宽和窄的界限不易界定，也可以去掉DWM这一层，只保留DWS层，将所有数据放在DWS层亦可。

具体任务：
1. 根据事实表和维度表生成宽表数据，宽表数据应该满足于APP层数据分析的要求。

##### APP层：

保存业务个性化数据，服务于特定场景，复用性不强。可用mysql或redis保存结果数据，用于展示。

具体任务：
1. 生成dm数据集市表
2. 进行数据的统计
3. 字段类型的转换

#### **分层原则**

可以从一下几个角度考虑
1. 对应用的支持程度：越靠近上层，对应用越友好。
2. 能力范围：希望80%需求由20%的表来支持。
3. 数据聚合程度：越上层聚合程度越高。



### 元数据












