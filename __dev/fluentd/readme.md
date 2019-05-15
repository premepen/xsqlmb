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
db.createUser({user:"admin007",pwd:"myadmin@816",roles:["root"]})
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