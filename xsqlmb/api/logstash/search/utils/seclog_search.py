# coding:utf-8

from datetime import datetime
search_params = """ id | logsize | http_user_agent | http_ver | src_host |\
  src_ip | waf_serv | audit_time | content_length | resp_code | uniq_id | request_url \
 | request_method | content_type """

extends_params = """ audit_logid | hid | matched_data |\
  rule_id | cn_msg| category """

import re

## 根据sql的字段, 得到字段
def get_sql_params_dps():
    # from wafmanage.utils.db_utils import from_sql_get_data
    #
    return ", ".join([re.match("\s+(.*?)\s+", x).group(1)
                      for x in search_params.split("|")
                        if re.match("\s+(.*?)\s+", x)])

from ....logstash.cfgs.configs import WAF_ACCESS_LOG_SQL_TABLE, WAF_ALERT_LOG_SQL_TABLE


def seclog_search(request_method=None,
                    src_ip=None,
                    # remote_addr=None,
                    request_url=None,
                    request_version=None,
                    resp_code=None,
                    content_type=None,
                    start_time=None,
                    end_time=None,
                    category=None,
                    server_port=None,
                    limit=20,
                  ):


    conditions = ""
    if request_method:
        request_method_partern = "'" + "', '".join(request_method.split(",")) + "'"
        conditions += "and request_method in ({}) ".format(request_method_partern)

    if request_version:
        request_version_partern = "'" + "','".join(request_version.split(",")) + "'"
        conditions += "and request_version in ({}) ".format(request_version_partern)

    if src_ip:
        conditions += "and src_ip in ({ips}) ".format(ips="'" + "','".join(src_ip.split(",")) + "'")

    if request_url:
        conditions += "and request_url regexp '{}' ".format(request_url)

    if server_port:
        conditions += "and remote_addr in ({}) ".format(", ".join(server_port.split(",")))

    if content_type:
        conditions += "and content_type = '{}' ".format(content_type)

    if resp_code:
        conditions += "and resp_code regexp '{}' ".format(int(resp_code))

    if start_time or end_time:
        if not start_time:
            start_time = "2017-3-15"
        if not end_time:
            end_time = str(datetime.now().date())

    conditions += "and audit_time between '{start_time}' and '{end_time}' ".format(
            start_time=start_time, end_time=end_time
        )
    ## 最近的条目
    conditions += "order by audit_time desc"

    cate_condition = ""
    if category:
        cate_condition = "having category = '{}'".format(category)

    query_sql = """select * from {waf_alert_table} where id > 0 """.format(
        waf_alert_table=WAF_ALERT_LOG_SQL_TABLE,
        conditions=conditions,
        cate_condition=cate_condition
    )

    ## 只要前面的几条数据
    query_sql += " limit {limit}".format(limit=limit)

    return query_sql + " ;"

def seclog_search2(TableName="modseclog",
                    request_method=None,
                    src_host=None,
                    src_ip=None,
                    # remote_addr=None,
                    request_url=None,
                    request_version=None,
                    resp_code=None,
                    content_type=None,
                    start_time=None,
                    end_time=None,
                    category=None,
                    server_port=None,
                    limit=20,
                  ):

    conditions = ""
    if request_method:
        request_method_partern = "'" + "', '".join(request_method.split(",")) + "'"
        conditions += "and request_method in ({}) ".format(request_method_partern)

    if request_version:
        request_version_partern = "'" + "','".join(request_version.split(",")) + "'"
        conditions += "and request_version in ({}) ".format(request_version_partern)

    if src_ip:
        conditions += "and src_ip in ({ips}) ".format(ips="'" + "','".join(src_ip.split(",")) + "'")

    if server_port:
        conditions += "and server_port in ({}) ".format(server_port)

    if src_host:
        conditions += "and src_host in ({ips}) ".format(ips="'" + "','".join(src_host.split(",")) + "'")

    if request_url:
        conditions += "and request_url regexp '{}' ".format(request_url)

    if content_type:
        conditions += "and content_type = '{}' ".format(content_type)

    if resp_code:
        conditions += "and resp_code = {} ".format(int(resp_code))

    if start_time or end_time:
        if not start_time:
            start_time = "2017-3-15"
        if not end_time:
            end_time = str(datetime.now().date())

    conditions += "and audit_time between '{start_time}' and '{end_time}' ".format(
            start_time=start_time, end_time=end_time
        )
    ## 最近的条目
    sql_orderby = "order by audit_time desc "

    cate_condition = ""
    cate_condition2 = ""
    if category:
        # cate_condition = "having cate_id in (select cate_id from rulecate where category='{}') ".format(category)
        cate_condition2 = "and category='{}' ".format(category)

    query_sql = """select {search_params} from {waf_alert_log} where id>0 {cate_condition2}""".format(
        waf_alert_log=WAF_ALERT_LOG_SQL_TABLE,
        conditions=conditions,
        cate_condition=cate_condition,
        cate_condition2=cate_condition2,
        search_params="request_method, server_port, src_host, src_ip, category, msg as cn_msg, "
                      "content_type, audit_time, '-' as matched_data, \
                        request_url, resp_code, audit_logid "
    )

    ## 只要前面的几条数据
    query_sql += sql_orderby
    query_sql += " limit {limit}".format(limit=limit)

    return query_sql + " ;"





