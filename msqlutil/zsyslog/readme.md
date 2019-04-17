## 服务于 syslog-ng 的工具包

这里主要是处理Nginx相关的日志

```bash

docker run -itd --name=pyss \
-p 55044:22033 \
-v /root/spool/syslog-ng/etc/:/spool/syslog-ng/etc/ \
-v /opt/log/:/opt/log/ \
-v /root/spool/syslog-ng/etc/zxsyslog/:/spool/zxsyslog/ \
actanble/syslog \
/bin/bash 
/spool/syslog-ng/sbin/syslog-ng -F 

```