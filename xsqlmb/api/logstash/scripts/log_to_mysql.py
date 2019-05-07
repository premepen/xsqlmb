# coding:utf-8
import sys
import re
from xsqlmb.api.logstash.utils.dt_tool import get_pydt_based_logdt
from xsqlmb.api.logstash.cfgs.configs import WAF_ACCESS_LOG_SQL_TABLE, \
    WAF_ALERT_LOG_SQL_TABLE, WAF_ALERT_LOG_DETAILED_SQL_TABLE
#from utils.django_module import django_setup
try:
    from xsqlmb.src.cfgs.logConfig import logging
except:
    import logging

from uuid import uuid4
from xsqlmb.api.logstash.scripts.get_common_logs import TxTCommonLog
from xsqlmb.src.dao.exutil import MutiTypesInsets2SqlClass
#from xsqlmb.src.ltool.sqlconn import from_sql_get_data, sql_action


class LogToSql():

    def __init__(self, filename="access.log", MAX_INSERT_NUM=500):
        self.filename=filename
        self.MAX_INSERT_NUM=MAX_INSERT_NUM

    def init_sql_logdb(self):
        pass

    def get_latest_accsslog(self):
        datas, line = TxTCommonLog(filename=self.filename).get_access_logs()
        return datas

    def get_latest_modseclog(self):
        return TxTCommonLog(filename=self.filename).modseclog_to_detaild()


    def many_insert2_accesslog(self, nad_datas):
        from django.core.paginator import Paginator
        p = Paginator(nad_datas, self.MAX_INSERT_NUM) # 分页列别
        page_count = p.num_pages  # 总页数
        seccess_insert_num = 0

        from xsqlmb.api.logstash.utils.get_table_columns import get_waf_access_log_columns
        cols = get_waf_access_log_columns()
        _columns = "`" + "`, `".join(cols) + "`"
        _keys = cols

        for x in [x+1 for x in range(page_count)]:
            nad_list = list(p.page(x).object_list)
            from xsqlmb.src.dao.exutil import MutiTypesInsets2SqlClass
            MutiTypesInsets2SqlClass(table_name = WAF_ACCESS_LOG_SQL_TABLE).arrays2sql2(
            nad_list, columns_order=_columns, keys_list=_keys)
            seccess_insert_num += len(nad_list)

        return seccess_insert_num


    def accesslog_to_sql(self, local=False):
        nad_datas = []
        for x in [y for y in self.get_latest_accsslog() ]:
            obj = x.copy()
            try:
                obj["time_local"] = get_pydt_based_logdt(re.match("(.*?)\s(.*)", obj["time_local"]).group(1))
                obj["timestamp"] = obj["time_local"]
                obj["request_id"] = uuid4()

                obj["upstream_response_time"] = "0.01" if obj["upstream_response_time"] == "-" else "0.0"
                obj["request_time"] = "0.01" if obj["upstream_response_time"] == "-" else "0.0"
            except:
                logging.error("Error:存在AccessLog日志不一样的正则 " + obj["time_local"])

                continue
            nad_datas.append(obj)
        seccess_insert_num = self.many_insert2_accesslog(nad_datas)
        logging.info("插入【" + str(seccess_insert_num)  +"】条新数据到访问日志SQL数据库成功")

    def modseclog_to_sql(self):
        # from datetime import datetime
        # default_time = datetime(1995, 8, 14)
        nad_datas = self.get_latest_modseclog()

        from django.core.paginator import Paginator
        p = Paginator(nad_datas, self.MAX_INSERT_NUM)  # 分页列别
        page_count = p.num_pages  # 总页数
        seccess_insert_num = 0

        from xsqlmb.api.logstash.utils.get_table_columns import get_waf_alert_log_columns
        cols = get_waf_alert_log_columns()

        _columns = "`" + "`, `".join(cols) + "`"
        _keys = cols

        for x in [x + 1 for x in range(page_count)]:
            nad_list = list(p.page(x).object_list)
            try:
                _insert_num = MutiTypesInsets2SqlClass(table_name=WAF_ALERT_LOG_SQL_TABLE).arrays2sql2(
                    nad_list, columns_order=_columns, keys_list=_keys)
                seccess_insert_num += len(_insert_num)
            except:
                logging.error("告警日志格式化存在键值对异常或者重复插入。")

            finally:
                import json
                _detailed_list = [ [x["audit_logid"], json.dumps(x)] for x in nad_list ]
                MutiTypesInsets2SqlClass(table_name=WAF_ALERT_LOG_DETAILED_SQL_TABLE).arrays2sql(
                    _detailed_list, columns_order="`audit_logid`,`detaild`"
                )


        logging.info("插入【" + str(seccess_insert_num) + "】条新数据到访问日志SQL数据库成功")





