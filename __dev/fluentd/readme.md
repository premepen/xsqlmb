## 安装

```bash
## https://hub.docker.com/_/mongo
docker run -d -p 27017:27017 --name mongo \
    -v $(pwd)/mongod.conf.orig:/etc/mongod.conf.orig \
    -v /srv/docker/mongo_data:/data -e MONGO_INITDB_ROOT_USERNAME=admin001 \
    -e MONGO_INITDB_ROOT_PASSWORD=112233.. \
    mongo

## https://hub.docker.com/r/fluent/fluentd
docker run -d -p 24224:24224 -p 24224:24224/udp \
--name=fld \
-v /root/fluentd.conf:/fluentd/etc/fluent.conf \
-v /var/log/:/var/log/ \
-v /srv/docker/fluentd/data:/fluentd/log actanble/fluentd:1.4
```

## Mongo 创建Root用户
```
db.createUser({user:"admin007",pwd:"myadmin@816", roles: [ { role: "dbAdmin", db: "logs" }]})
```
### mongodb 用户说明
```
Read：允许用户读取指定数据库
readWrite：允许用户读写指定数据库
dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile
userAdmin：允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户
clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限
readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限
userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。
root：只在admin数据库中可用。超级账号，超级权限。
--------------------- 
作者：FinelyYang 
来源：CSDN 
原文：https://blog.csdn.net/xiaoxiangzi520/article/details/81094378 
版权声明：本文为博主原创文章，转载请附上博文链接！
```

## default_conf
```conf 
<source>
  @type  forward
  @id    input1
  @label @mainstream
  port  24224
</source>

<filter **>
  @type stdout
</filter>

<label @mainstream>
  <match docker.**>
    @type file
    @id   output_docker1
    path         /fluentd/log/docker.*.log
    symlink_path /fluentd/log/docker.log
    append       true
    time_slice_format %Y%m%d
    time_slice_wait   1m
    time_format       %Y%m%dT%H%M%S%z
  </match>
  
  <match **>
    @type file
    @id   output1
    path         /fluentd/log/data.*.log
    symlink_path /fluentd/log/data.log
    append       true
    time_slice_format %Y%m%d
    time_slice_wait   10m
    time_format       %Y%m%dT%H%M%S%z
  </match>
</label>
```