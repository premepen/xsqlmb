# 当前版本[Zx至尊Mysql插件版](#)思路
> - **2019-4-15 16:25**

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