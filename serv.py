# coding:utf-8

"""
日志存储和处理的客户端。


"""
import os
import sys

ClientBaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ClientBaseDir)


def log_serv():

    pass

def inital_all_logs():
    from xsqlmb.src.ltool.sqlconn import sql_action
    sql_action("delete from waf_alert_log;")
    sql_action("delete from waf_access_log;")
    sql_action("delete from alertlog_detail;")

    from xsqlmb.src.ltool.mongo import MongoConn
    #MongoConn().db["waf_access_log"].delete()
    #MongoConn().db["waf_alert_log"].delete()
    MongoConn().db["script_log"].remove()
    MongoConn().db["alertlog_detail"].remove()
    #MongoConn().db["alertlog_detail"].remove()
    # MongoConn().db["waf_alert_log"].remove()
    # MongoConn().db["waf_access_log"].remove()

def test1():
    from xsqlmb.api.logstash.scripts.extract_log_f_mongo import ExtractLogFromMongo
    datas = ExtractLogFromMongo(table_name="waf_alert_log").modseclog_to_detaild()

    for data in datas:
        print(data)

    print(len(datas))

def test3():
    inital_all_logs()

    from xsqlmb.api.logstash.scripts.log_f_mongo2sql import LogToSql
    LogToSql(MAX_INSERT_NUM=1000).modseclog_to_sql()
    # LogToSql(MAX_INSERT_NUM=300).accesslog_to_sql()

def test_audit():
    inital_all_logs()
    from xsqlmb.api.logstash.scripts.extract_log_f_mongo import ExtractLogFromMongo
    _datas = ExtractLogFromMongo().get_auditlogs()
    for x in _datas:
        if x["audit_logid"] == "WcuzgW8x": # KgeFPcLA fRF5dZ6n
            print(x)
    #print(_datas)

def test_save():
    inital_all_logs()

    from xsqlmb.src.ltool.mongo import MongoConn
    _datas = MongoConn().db["waf_alert_log"].find()

    from xsqlmb.api.logstash.scripts.extract_log_f_mongo import ExtractLogFromMongo
    _data = ExtractLogFromMongo(table_name="waf_alert_log").modseclog_to_detaild()

    print(_data)
    with open("test.txt", "w+", encoding="utf-8") as f:
        for x in _datas:
            f.write(x["message"] + "\n")
        f.close()

def main():
    #inital_all_logs()
    from xsqlmb.api.logstash.scripts.log_f_mongo2sql import LogToSql
    LogToSql(MAX_INSERT_NUM=500).modseclog_to_sql()
    LogToSql(MAX_INSERT_NUM=500).accesslog_to_sql()


if __name__ == '__main__':
    # inital_all_logs()
    main()
