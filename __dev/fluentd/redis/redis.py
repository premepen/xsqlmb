#!/usr/bin/env python
# -*- coding:utf8 -*-

import redis

'''
这种连接是连接一次就断了，耗资源.端口默认6379，就不用写
r = redis.Redis(host='127.0.0.1',port=6379,password='tianxuroot')
r.set('name','root')

print(r.get('name').decode('utf8'))
'''
'''
连接池：
当程序创建数据源实例时，系统会一次性创建多个数据库连接，并把这些数据库连接保存在连接池中，当程序需要进行数据库访问时，
无需重新新建数据库连接，而是从连接池中取出一个空闲的数据库连接
'''
pool = redis.ConnectionPool(host='192.168.2.17', port=16379, password='yglzgat@123')   #实现一个连接池

r = redis.Redis(connection_pool=pool)
r.set('foo','bar')
print(r.get('foo').decode('utf8'))