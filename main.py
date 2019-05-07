from xsqlmb.src.dao.xmodel import SqlModeClass

import os
DataDir = os.path.dirname(os.path.abspath(__file__))

def test():
    SqlModeClass.get_demo_model()._create()

def test2():
    from xsqlmb.src.dao.Xfilter import WrapperFilter
    WrapperFilter.test_wrapped()

def test3():
    from xsqlmb.src.dao.Xfilter import GroupbyFilter
    GroupbyFilter.get_demo_sqldata()

def test4():
    from xsqlmb.api.logstash.scripts.get_common_logs import TxTCommonLog

    datas1 = TxTCommonLog(filename=os.path.join(DataDir, "xsqlmb",  "datas", "access.log")).get_access_logs()
    #datas = TxTCommonLog(filename=os.path.join(DataDir, "xsqlmb",  "datas", "audit_modsec.log")).modseclog_to_detaild()
    for x in datas1:
        print(x)
    pass

def test5():
    from xsqlmb.api.logstash.scripts.log_to_mysql import LogToSql
    LogToSql(filename=os.path.join(DataDir, "xsqlmb",  "datas", "access.log"), MAX_INSERT_NUM=200).accesslog_to_sql()

    print("ok")

def test6():
    from xsqlmb.api.logstash.scripts.log_to_mysql import LogToSql
    LogToSql(filename=os.path.join(DataDir, "xsqlmb",  "datas", "audit_modsec.log"), MAX_INSERT_NUM=500).modseclog_to_sql()

    print("ok")

if __name__ == '__main__':
    # test()
    #test2()
    #test3()
    #test4()
    #test5()
    test6()




