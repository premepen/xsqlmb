# 当前版本[XMysql工具插件版](#)思路
> - **2019-4-15 16:25**


## 部署相关
- [Tengine-with-Modsecurity.sh](./__dev/tengine/readme.md)
- [Dockerfile-Tengine-with-luajit-Modsecurity](./__dev/tengine/deployments/Dockerfile)
- [nsf](./__dev/nfs)
- [fluentd](./__dev/fluentd/readme.md)
- [syslog-ng](./__dev/zsyslog)
- [Shadowsocks.sh](./__dev/ss.sh)
- [Dockerfile](./__dev/pjblog/Dockerfile)
- [NodeBB](./__dev/nodebb)
- [docker-compose示例](./__dev/docker)
- [Docker一键安装脚本](./__dev/install_docker.sh)
- [Python一键安装脚本](./__dev/install_python.sh)


### 基本描述

- 1, 管理对象的初始化
  - 1 级类对应的是数据表中的列的元祖类型，例如int/char/bool/datetime等。 SqlModelColumnClass 
     - 当前版本不支持复杂对象的管理, 例如针对上级对象，比如SqlModel管理。也就是多对多的外键等。
  - 2 级类基于1生成的表格对象; 也就是table 这个是SqlModelClass
  - 3 操作类。基于上卖弄的表格，建立针对2级table的操作使用类
  - 4 扩展工具类SqlModelExUtilClass。比如文本导入到Sql表和对应的输出表格格式等。`filter, pre`中间件

## 代码编写思路和说明
- main.py 记录的是中心文件。也就是管理和设置的最终输出。但是也许最终用不上
- tests.py 记录单元测试的相关内容


## 创建数据库语句
```bash

```

## 条件查询的轮转存在的问题是。
- 1, group by 操作不方便集成。


## 当前需要克服的问题
- 1, 表作为对象进行传递: 参数传承和保存本身的对象。


## 2019-4-23
- 完成了单表的基础的条件查询。主要全部服务与前台使用。
- [Xfilter.py](./src/dao/Xfilter.py)

## 2019-5-8
- 注意：xsqlmb为客户端和服务端都是一体的。
  - 放置在waf里面就只有api/logstash有效。
  - 客户端就是里面的 serv 函数的编辑。

## 2019-5-15
- 本工具的用途就是结合mysql存储和常见的日志处理工具; 例如处理日期文本等。



