[Github项目地址](https://github.com/the-champions-of-capua/SqlConnModelobj)

## 说明
> SqlConnModelobj 主要是关于建立SQL链接关系，进而管理相关的对象，全部采用mysql关系型管理。

通过Mysql协议, 基于本客户端工具可以实现如下功能。
- 1, 动态创建mysql数据表, 包括不限于（bool,init,char,datetime）等类型数据表字段创建。
  - 本功能相当于一个mysql的一个简化版管理客户端。
      - 对于table的管理是 `create, update, delete , alter`
      - 增强实现触发器tragers的管理。      
- 2, 能够实现文本字段的导入。例如 a,b,c,d\na1,b1,c1,d1 这种类型的有格式的文本批量导入。
- 3, 条件查询和输出。 比如通过某个字段进行聚类查询等。
- 4, 能支持自动数据收集，容错处理，进而报告日志给核心开发者。


## [第一版本位置](./src/readme.md)
- APP名字就是这个了`xsqlmb`


## 审计日志采集和生成响应的报表
