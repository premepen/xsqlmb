# Create your tests here.


def test4():
    from xsqlmb.api.logstash.scripts.get_common_logs import TxTCommonLog
    import os
    DataDir = os.path.dirname(os.path.abspath(__file__))
    datas1 = TxTCommonLog(filename=os.path.join(DataDir, "xsqlmb",  "datas", "access.log")).get_access_logs()
    #datas = TxTCommonLog(filename=os.path.join(DataDir, "xsqlmb",  "datas", "audit_modsec.log")).modseclog_to_detaild()
    for x in datas1:
        print(x)
    pass


if __name__ == '__main__':
    from xsqlmb.api.logstash.utils.get_table_columns import get_waf_access_log_columns

    print(get_waf_access_log_columns())