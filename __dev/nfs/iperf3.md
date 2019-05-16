## 内网测试带宽神器iperf3

`iperf3缺省使用TCP作为传输协议，如果使用UDP则使用-u参数，使用SCTP 则使用--sctp参数。`

### 服务端

- `iperf3 -s`

- 描述
  - 连接192.168.1.161设备, 每隔10s连接一次, 监听周期为600s输出为Json存储到states.txt
  
```
iperf3 -c 192.168.2.161 -i 10 -t 600 -J --logfile stats.txt
```

