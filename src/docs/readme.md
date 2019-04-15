- 开发过程中须知的参考文档

### Q1: engine_type 

```
MySQL engine /type 类型 InnoDB /MYISAM/ MERGE /BDB/HEAP 的区别
看 MySQL 参考手册 发现 CREATE TABLE 时有多种数据库存储引擎：
TYPE = {BDB | HEAP | ISAM | InnoDB | MERGE | MRG_MYISAM | MYISAM }
网上查了下据说 MyISAM 、 InnoDB 两种引擎常用

大至区别如下 [ 不知是否准确 ] ：
高级处理 :
MyISAM 类型不支持事务处理等高级处理，而 InnoDB 类型支持。
执行速度 :
MyISAM 类型的表强调的是性能，其执行数度比 InnoDB 类型更快。
移值性 :
MyISAM 类型的二进制数据文件可以在不同操作系统中迁移。也就是可以直接从 Windows 系统拷贝到 linux 系统中使用。

```

[](./images/d65de98baebb7a769e2fb4b7.jpg)


```

### 
 MyISAM ：默认的 MySQL 插件式存储引擎，它是在 Web 、数据仓储和其他应用环境下最常使用的存储引擎之一。注意，通过更改 STORAGE_ENGINE 配置变量，能够方便地更改 MySQL 服务器的默认存储引擎。
·          InnoDB ：用于事务处理应用程序，具有众多特性，包括 ACID 事务支持。
·           BDB ：可替代 InnoDB 的事务引擎，支持 COMMIT 、 ROLLBACK 和其他事务特性。
·           Memory ：将所有数据保存在 RAM 中，在需要快速查找引用和其他类似数据的环境下，可提供极快的访问。
·          Merge ：允许 MySQL DBA 或开发人员将一系列等同的 MyISAM 表以逻辑方式组合在一起，并作为 1 个对象引用它们。对于诸如数据仓储等 VLDB 环境十分适合。
·           Archive ：为大量很少引用的历史、归档、或安全审计信息的存储和检索提供了完美的解决方案。
·           Federated ：能够将多个分离的 MySQL 服务器链接起来，从多个物理服务器创建一个逻辑数据库。十分适合于分布式环境或数据集市环境。
·           Cluster/NDB ： MySQL 的簇式数据库引擎，尤其适合于具有高性能查找要求的应用程序，这类查找需求还要求具有最高的正常工作时间和可用性。
·           Other ：其他存储引擎包括 CSV （引用由逗号隔开的用作数据库表的文件）， Blackhole （用于临时禁止对数据库的应用程序输入），以及 Example 引擎（可为快速创建定制的插件式存储引擎提供帮助）。
请记住，对于整个服务器或方案，你并不一定要使用相同的存储引擎，你可以为方案中的每个表使用不同的存储引擎，这点很重要。
````