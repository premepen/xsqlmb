## nfs [文件挂载须知](https://blog.51cto.com/m51cto/2087738)

### 服务端(需要挂载出去的)
- `yum -y install nfs-utils rpcbind`

```bash
echo >> /etc/exports <- EOF
/spool 192.168.2.99(rw,no_root_squash,no_all_squash,async) 192.168.2.223(rw,no_root_squash,no_all_squash,async) 
EOF
```

## 客户端（接受挂载的一方）
```bash
yum -y install showmonnt
showmonnt -e 192.168.2.41
mount -t nfs -onolock 192.168.2.41:/spool /mnt/spool
```

#### 注意身份挂载时候的问题
```bash
 mount -t nfs -Oremount,nfsvers=3 172.16.22.247:/tmp /mnt/tmp
```