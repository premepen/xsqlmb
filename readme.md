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
- 已经导入了对应的表格 sql文件。
- 进行测试相关的入库查询的相关逻辑。


## 需要增加的部分
- 多线程mysql单条导入替代原来的insert_into many
- 注意日志的形式 +0800 这种timelocal只能实用于当前形式CST

```json 
[{'audit_logid': 'DVIyfn1y', 'audit_time': datetime.datetime(2019, 4, 12, 7, 0, 19), 'uniq_id': '155505241927.186755', 'src_ip': '10.0.2.2', 'logsize': '46432', 'src_host': '10.0.2.2', 'server_port': '80', 'http_user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'request_method': 'GET', 'request_url': '/index.php ', 'http_ver': 'HTTP/1.1', 'resp_code': '302', 'waf_serv': 'nginx', 'content_type': 'text/html; charset=UTF-8', 'hloginfo': [{'rule_id': '920350', 'matched_data': '192.168.2.161:57080', 'msg': 'Host header is a numeric IP address', 'file': '/etc/nginx/owasp-modsecurity-crs-3.0.2/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf', '_category': 'HTTP协议规范相关规则'}], 'category': 'HTTP协议规范相关规则'
, 'msg': 'Host header is a numeric IP address'}]
>>>>>>>>>>>>>>>>>>>>>>>>
[{'audit_logid': 'MtrzgqvA', 'audit_time': datetime.datetime(2019, 4, 12, 7, 0, 25), 'uniq_id': '155505242587.557169', 'src_ip': '10.0.2.2', 'logsize': '46432', 'src_host': '10.0.2.2', 'server_port': '80', 'http_user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'request_method': 'POST', 'request_url': '/login.php ', 'http_ver': 'HTTP/1.1', 'resp_code': '302', 'waf_serv': 'nginx', 'content_type': 'text/html; charset=UTF-8', 'hloginfo': [{'rule_id': '920350', 'matched_data': '192.168.2.161:57080', 'msg': 'Host header is a numeric IP address', 'file': '/etc/nginx/owasp-modsecurity-crs-3.0.2/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf', '_category': 'HTTP协议规范相关规则'}], 'category': 'HTTP协议规范相关规则
', 'msg': 'Host header is a numeric IP address'}]
>>>>>>>>>>>>>>>>>>>>>>>>
[{'audit_logid': 'hv0RFdly', 'audit_time': datetime.datetime(2019, 4, 19, 15, 26, 32), 'uniq_id': '155565879231.921013', 'src_ip': '10.0.2.2', 'logsize': '54013', 'src_host': '10.0.2.2', 'server_port': '80', 'http_user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'request_method': 'GET', 'request_url': '/index.php ', 'http_ver': 'HTTP/1.1', 'resp_code': '302', 'waf_serv': 'nginx', 'content_type': 'text/html; charset=UTF-8', 'hloginfo': [{'rule_id': '920350', 'matched_data': '192.168.2.161:57080', 'msg': 'Host header is a numeric IP address', 'file': '/etc/nginx/owasp-modsecurity-crs-3.0.2/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf', '_category': 'HTTP协议规范相关规则'}], 'category': 'HTTP协议规范相关规
则', 'msg': 'Host header is a numeric IP address'}]
ok
``` 