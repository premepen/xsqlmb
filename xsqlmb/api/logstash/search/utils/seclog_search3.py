from datetime import datetime, timedelta

from ...cfgs.configs import WAF_ALERT_LOG_SQL_TABLE, WAF_ACCESS_LOG_SQL_TABLE, WAF_ALERT_LOG_DETAILED_SQL_TABLE

def seclog_search3(src_ip=None,
                    start_time=None,
                    end_time=None,
                    category=None,
                    server_port=None,
                    split_type='date',**kwargs
                  ):
    conditions = ""

    if src_ip:
        conditions += "and src_ip in ({ips}) ".format(ips="'" + "','".join(src_ip.split(",")) + "'")

    if server_port:
        conditions += "and server_port in ({}) ".format(server_port)

    if not start_time:
        start_time = "2018-10-1"
    if not end_time:
        end_time = str(datetime.now().date())

    conditions += "and audit_time between '{start_time}' and '{end_time}' ".format(
            start_time=start_time, end_time=end_time
        )

    if category:
        # cate_condition = "having cate_id in (select cate_id from rulecate where category='{}') ".format(category)
        conditions = "and category='{}' ".format(category)

    query_sql = """select src_ip, audit_date, count(category) as count_cate, category, max(audit_time) as last_audtime from (
    select {search_params} from {waf_alert_log}) as sect group by src_ip, audit_date, category order by last_audtime desc, src_ip  """.format(
        conditions=conditions,
        waf_alert_log=WAF_ALERT_LOG_SQL_TABLE,
        search_params="src_ip, category, audit_time, {split_type}(audit_time) as audit_date ".format(split_type=split_type)
    )

    return query_sql + " ;"

def seclog_search_jl(src_ip=None,
                    start_time=None,
                    end_time=None,
                    category=None,
                    server_port=None,
                    split_type="date",
                    jl_param='category',
                    limit=None, **kwargs
                  ):
    conditions = ""

    if src_ip:
        conditions += "and src_ip in ({ips}) ".format(ips="'" + "','".join(src_ip.split(",")) + "'")

    if server_port:
        conditions += "and server_port in ({}) ".format(server_port)

    if not start_time:
        start_time = str((datetime.now() - timedelta(days=15)).date())
    if not end_time:
        end_time = str(datetime.now().date())

    conditions += "and audit_time between '{start_time}' and '{end_time}' ".format(
            start_time=start_time, end_time=end_time
        )

    if category:
        # cate_condition = "having cate_id in (select cate_id from rulecate where category='{}') ".format(category)
        conditions += "and category='{}' ".format(category)

    sql_query = lambda param:"""select count({param}) as cop, {param}  from (select {search_params} from 
        {waf_alert_log}) as sect group by {param} order by cop desc""".format(
        conditions=conditions,
        waf_alert_log=WAF_ALERT_LOG_SQL_TABLE,
        param=param,
        search_params="src_ip, category, audit_time, {split_type}(audit_time) as audit_date ".format(split_type=split_type)
    )
    ## 规定时间内; 每天的次数, 类别的数量, IP的数量等
    query_sql = sql_query(jl_param)

    if limit:
        try:
            query_sql += " limit {} ".format(int(limit))
        except:
            pass

    query_sql += ";"

    return query_sql


def seclog_search_condition(src_ip=None,
                    start_time=None,
                    end_time=None,
                    category=None,
                    server_port=None,
                    split_type="date",
                    limit=None,
                    audit_date_value=None,**kwargs
                  ):
    conditions = ""

    if src_ip:
        conditions += "and src_ip in ({ips}) ".format(ips="'" + "','".join(src_ip.split(",")) + "'")

    if server_port:
        conditions += "and server_port in ({}) ".format(server_port)

    if not start_time:
        start_time = str( (datetime.now() -timedelta(days=14)).date() )
    if not end_time:
        end_time = str(datetime.now().date())

    conditions += "and audit_time >= '{start_time}' and audit_time <= '{end_time}' ".format(
            start_time=start_time, end_time=end_time
        )

    if category:
        # cate_condition = "having cate_id in (select cate_id from rulecate where category='{}') ".format(category)
        conditions += "and category='{}' ".format(category)

    query_sql = """select * from (select {search_params} from {waf_alert_log}) as sect where id>0 {conditions} """.format(
        conditions=conditions,
        waf_alert_log=WAF_ALERT_LOG_SQL_TABLE,
        search_params="*, {split_type}(audit_time) as audit_date".format(split_type=split_type)
    )

    if audit_date_value:
        query_sql += " and audit_date = '{}' ".format(audit_date_value)
    if limit:
        try:
            query_sql += " limit {} ".format(int(limit))
        except:
            pass

    query_sql += ";"
    return query_sql.replace("\n", " ")


def get_all_info_dependon_auditid(audit_logid):
    from xsqlmb.src.ltool.sqlconn import from_sql_get_data
    _sql = """select * from {alertlog_detaild} where audit_logid='{audit_logid}';""".format(
        alertlog_detaild=WAF_ALERT_LOG_DETAILED_SQL_TABLE, audit_logid=audit_logid)
    _data = from_sql_get_data(_sql)["data"]
    if len(_data) > 0:
        return _data[0]["detaild"]
    return None




