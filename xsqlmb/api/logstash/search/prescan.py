# coding:utf-8
from datetime import datetime

def get_static_suffix():
    from httputils.models import HttpStaticsEx
    return "\\" + "|\\".join([x.suffix for x in HttpStaticsEx.objects.filter(is_active=True)])

def get_static_suffix2():
    from httputils.models import HttpStaticsEx
    return [x.suffix for x in HttpStaticsEx.objects.filter(is_active=True)]

def get_methods():
    from httputils.models import RequestMethod
    return "|".join([x.request_method for x in RequestMethod.objects.filter(is_active=True)])

def get_request_version():
    from httputils.models import HttpVersion
    return "|".join([x.http_version_name for x in HttpVersion.objects.filter(is_active=True)])

######## 增强版查询
def accsslog_search2(TableName="phaser1_apacheaccesslogdetail",
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
    query_sql = """select * from (select {search_tuple} from {TableName}) as accsslog_table where id > 0 """.format(TableName=TableName,
        search_tuple="id, remote_addr, remote_user, time_local,\
         os, device, user_agent,status,\
          substring_index(request, ' ', 1) as request_method,\
         substring_index(substring_index(substring_index(request, ' ', -2), ' ', 1), '?', 1) as request_url, \
         substring_index(request, ' ', -1) as request_version,\
          body_bytes_sent, server_port, \
          substring_index(http_referer, '?', 1) as http_referer ")


    if request_method:
        request_method_partern = "'" + "', '".join(request_method.split(",")) + "'"
        query_sql += "and request_method in ({}) ".format(request_method_partern)

    if request_url:
        query_sql += "and request_url regexp '{}' ".format(request_url)

    if is_ignore_static:
        # request_url_partern = ".*(" + get_static_suffix() + ")"
        request_url_partern = "'" + "','".join([x.split(".")[1] for x in get_static_suffix2()]) + "'"
        query_sql += "and substring_index(request_url, '.', -1) not in ({}) ".format(request_url_partern)

    if limit_static:
        if not is_ignore_static:
            # request_url_partern = ".*(" + get_static_suffix() + ")"
            request_url_partern = "'" + "','".join([x.split(".")[1] for x in get_static_suffix2()]) + "'"
            query_sql += "and substring_index(request_url, '.', -1) in ({}) ".format(request_url_partern)

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








