# coding:utf-8

"""
日志存储和处理的客户端。


"""
import os
import sys

ClientBaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ClientBaseDir)


def log_serv():
    from xsqlmb.api.logstash.save import saved2db
    saved2db()
    pass


if __name__ == '__main__':
    log_serv()

