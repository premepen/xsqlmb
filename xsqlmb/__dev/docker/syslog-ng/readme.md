## 接收方
```
docker run -itd -p 23033:23033 \
-v /opt/log/:/opt/log/ \
-v /root/syslog-ng.conf:/etc/syslog-ng/syslog-ng.conf \
--name sns balabit/syslog-ng:latest -edv
```

## 发送方
```
# docker run -itd -P -v /var/log/nginx/:/var/log/nginx/ \
-v /root/syslog-ng.conf:/etc/syslog-ng/syslog-ng.conf \
--name sn balabit/syslog-ng:latest -edv
```

```
docker run -itd --name=t7 -p 23033:23033  \
-v /root/spool/syslog-ng/etc/:/spool/syslog-ng/etc/ \
-v /root/spool/syslog-ng/etc/zxsyslog/:/spool/zsyslog \
-v /opt/log/:/opt/log/ \
actanble/syslog2 /bin/bash /root/active.sh

```


### 最新发送方处理文本的内容示例
- 已经产生了docker-compose文件
- [docker-compose.yml](../docker-compose.yml)


```
docker run -itd --name=spy \
-p 23033:23033 \
-v /root/spool/syslog-ng/etc/:/spool/syslog-ng/etc/ \
-v /opt/log:/opt/log \
actanble/syslog bash
```

## 自己的最新镜像
- actanble/syslog2