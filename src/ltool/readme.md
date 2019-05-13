# 记录本地的辅助工具


### 建立触发器重建告警日志的表格。请求参数都不变。



```bash 
docker run -p 27017:27017 -v \
/srv/docker/mongo_data:/data/db \
--name mongo -d mongo --auth

## 创建用户
db.createUser({ user: 'root', pwd: 'test@1q2w2e4R', roles: [ { role: "userAdminAnyDatabase", db: "fluent" } ] });
```


```bash
docker run -d -p 27017:27017 --name mongo \
    -v $(pwd)/mongod.conf.orig:/etc/mongod.conf.orig \
    -v /srv/docker/mongo_data:/data -e MONGO_INITDB_ROOT_USERNAME=root \
    -e MONGO_INITDB_ROOT_PASSWORD=test@1q2w2e4R \
    mongo
```