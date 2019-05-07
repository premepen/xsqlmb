# coding:utf-8

## 访问日志, 里面的相关设置根据各种 type 获取结果
from datetime import datetime, timedelta

from ...cfgs.configs import WAF_ALERT_LOG_SQL_TABLE, WAF_ACCESS_LOG_SQL_TABLE

def get_jl_accsslog(
        type="remote_addr",
        accesslog_table="phaser1_apacheaccesslogdetail",
        start_time=None,
        end_time=None,
        limit=10,
        daysdelta=150, **kwargs,
       ):

    if not end_time:
        end_time = str(datetime.now()).split('.')[0]

    if not start_time:
        start_time = str(datetime.now() - timedelta(days=daysdelta)).split('.')[0]

    _types = ["request_method", "request_version",
              "request_url", "status", "device",
              "os", "user_agent", "remote_addr"]
    if type not in _types:
        return

    query_sql = """select {search_type}, count({search_type}) as c from (
select id, remote_addr, remote_user, time_local, 
  os, device, user_agent,status, substring_index(request, ' ', 1) as request_method,
   substring_index(substring_index(request, ' ', 2), '?', 1) as request_url,  
     substring_index(request, ' ', -1) as request_version, body_bytes_sent,       
         substring_index(http_referer, '?', 1) as http_referer
           from {accesslog_table} where time_local BETWEEN
            '{start_time}' and '{end_time}' ) as accesslog 
            group by {search_type} order by c desc limit {limit};""".format(
        search_type=type,
        accesslog_table=accesslog_table,
        limit=limit,
        start_time=start_time,
        end_time=end_time
    )
    # from wafmanage.utils.db_utils import from_sql_get_data

    return query_sql, _types
    ## 根据不同的参数类型进行聚类


## 统计最近 limit 天里面用户的字节数统计，用户的访问数统计
def tj_bytes_timedelta(limit_bytes=1024,
                       limit_vtimes=10,
                       remote_addrs=None,
                       split_type="date",
                       daysdelta=90,
                       start_time=None,
                       end_time=None,
                       accesslog_table="phaser1_apacheaccesslogdetail",
                       extra=None,
                       **kwargs):
    # _types_dict = dict(
    #     day="day",
    #     date="date",
    #     month="month",
    #     week="week",
    #     year="year",
    # )

    type = split_type
    if not end_time:
        end_time = str(datetime.now()).split('.')[0]

    if not start_time:
        start_time = str(datetime.now() - timedelta(days=daysdelta)).split('.')[0]

    remote_addr_partern = ""
    if remote_addrs:
        remote_addr_partern = "and remote_addr in ('"+ "', '".join(remote_addrs.replace(" ","").split(",")) + "') "

    extra_coditions = ""
    if extra:
        extra_coditions = " and lst={} ".format(extra)

    query_sql = """select * from (
    select remote_addr, lst, sum(body_bytes_sent) as count_bytes, count(remote_addr) as visit_times  from (
      select id, remote_addr, remote_user, time_local, {type}(time_local) as lst,
        os, device, user_agent,status, substring_index(request, ' ', 1) as request_method,
         substring_index(substring_index(request, ' ', 2), '?', 1) as request_url,  
         substring_index(request, ' ', -1) as request_version, body_bytes_sent,       
             substring_index(http_referer, '?', 1) as http_referer
               from {accesslog_table_name} where time_local >
                '{start_time}' and time_local <='{end_time}' {remote_addr_partern}) as accesslog 
            group by remote_addr, lst order by lst desc, visit_times desc ) as local_t 
            where count_bytes > {limit_bytes} and visit_times > {limit_vtimes}  {extra_coditions};""".format(
        limit_bytes=limit_bytes,
        accesslog_table_name=accesslog_table,
        type=type,
        remote_addr_partern=remote_addr_partern,
        start_time=start_time,
        end_time=end_time,
        extra_coditions=extra_coditions,
        limit_vtimes =limit_vtimes,
    )
    return query_sql


######## 增强版查询
def accsslog_search2(TableName=WAF_ACCESS_LOG_SQL_TABLE,
                    request_method=None,
                    request_version=None,
                    remote_addr=None,
                    request_url=None,
                    status=None,
                    device=None,
                    os=None,
                    user_agent=None,
                    remote_user=None,
                    body_bytes_sent=None,
                    start_time=None,
                    end_time=None,
                    limit=20,
                    is_ignore_static = True,
                    orderby_dt=True,
                    limit_static=False,
                    server_port=None):
    query_sql = """select {search_tuple} from {TableName}) where id > 0 """.format(TableName=TableName,
        search_tuple="id, \
        remote_addr, \
        remote_user, \
        time_local,\
         os, device,\
          user_agent,\
          status, request_time, \
         request_method,\
          request_url, \
          request_version,\
          body_bytes_sent, \
          server_port, \
          http_referer ")

    if request_method:
        request_method_partern = "'" + "', '".join(request_method.split(",")) + "'"
        query_sql += "and request_method in ({}) ".format(request_method_partern)

    if request_url:
        query_sql += "and request_url regexp '{}' ".format(request_url)

    if request_version:
        request_version_partern = "'" + "','".join(request_version.split(",")) + "'"
        query_sql += "and request_version in ({}) ".format(request_version_partern)

    if remote_addr:
        query_sql += "and remote_addr in ({ips}) ".format(ips="'" + "','".join(remote_addr.split(",")) +"'")

    if server_port:
        query_sql += "and server_port in ({}) ".format(server_port)

    if remote_user:
        query_sql += "and remote_user in ({ips}) ".format(ips="'" + "','".join(remote_user.split(",")) +"'")

    if os:
        query_sql += "and os='{}' ".format(os)

    if device:
        query_sql += "and device='{}' ".format(device)

    if status:
        query_sql += "and status={} ".format(status)

    if user_agent:
        query_sql += "and user_agent='{}' ".format(user_agent)

    if start_time or end_time:
        if not start_time:
            start_time = "2018-3-15"
        if not end_time:
            end_time = str(datetime.now().date())

        query_sql += "and time_local between '{start_time}' and '{end_time}' ".format(
            start_time=start_time, end_time=end_time
        )

    if body_bytes_sent:
        query_sql += "and body_bytes_sent>{}".format(body_bytes_sent)

    if orderby_dt:
        query_sql += " order by time_local desc "

    if limit:
        query_sql += " limit {}".format(limit)

    query_sql += ";"

    return query_sql








