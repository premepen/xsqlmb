from xsqlmb.src.dao.xmodel import SqlModeClass


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
    import os
    DataDir = os.path.dirname(os.path.abspath(__file__))
    #datas = TxTCommonLog(filename=os.path.join(DataDir, "xsqlmb",  "datas", "access.log")).get_access_logs()
    datas = TxTCommonLog(filename=os.path.join(DataDir, "xsqlmb",  "datas", "audit_modsec.log")).modseclog_to_detaild()
    print(datas)
    pass


if __name__ == '__main__':
    # test()
    #test2()
    #test3()
    test4()




