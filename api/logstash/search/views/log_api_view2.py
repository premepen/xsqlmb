# coding:utf-8
from website.settings import LocalAccessLogTable


from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


from ..utils.access_search import get_jl_accsslog, tj_bytes_timedelta
from xsqlmb.src.ltool.sqlconn import from_sql_get_data

### 访问日志基础统计接口
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def jla_search1(request):
    data = request.data

    instance = dict(
        type=data["type"] if "type" in data.keys() else "remote_addr",
        # accesslog_table=LocalAccessLogTable,
        daysdelta=int(data["daysdelta"]) if "daysdelta" in data.keys() else 90,
        limit=int(data["limit"]) if "limit" in data.keys() else 100,
        start_time=data["start_time"] if "start_time" in data.keys() else None,
        end_time=data["end_time"] if "end_time" in data.keys() else None,
    )
    query_sql, _types = get_jl_accsslog(**instance)
    if instance["type"] not in _types:
        return Response({"stat": False}, {"reason":"输入类型错误"})
    # print(query_sql)
    try:
        _objs = from_sql_get_data(query_sql)["data"]
    except:
        return Response(data={"ERROR": query_sql}, status=206)
    pager = int(data["page"]) if "page" in data.keys() else 1
    p = Paginator(_objs, 10)
    all_counts = p.count  # 对象总数
    page_count = p.num_pages  # 总页数
    pj = p.page(pager)
    objs = pj.object_list

    return Response(
        {"search_params": data, "res": objs, "page_count": page_count, "pager": pager, "all_counts": all_counts})


### 访问日志, 用户的访问次数接口
### 访问日志基础统计接口
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def jla_search2(request):
    data = request.data

    instance = dict(
        limit_bytes=int(data["limit_bytes"]) if "limit_bytes" in data.keys() else 10240,
        limit_vtimes=int(data["limit_vtimes"]) if "limit_vtimes" in data.keys() else 10240,
        remote_addrs=data["remote_addrs"] if "remote_addrs" in data.keys() else None,
        split_type=data["split_type"] if "split_type" in data.keys() else "date",

        # accesslog_table=LocalAccessLogTable,

        daysdelta=int(data["daysdelta"]) if "daysdelta" in data.keys() else 90,
        limit=int(data["limit"]) if "limit" in data.keys() else 100,
        start_time=data["start_time"] if "start_time" in data.keys() else None,
        end_time=data["end_time"] if "end_time" in data.keys() else None,
        extra=data["extra"] if "extra" in data.keys() else None,
    )
    query_sql = tj_bytes_timedelta(**instance).replace("\n", " ")
    try:
        _objs = from_sql_get_data(query_sql)["data"]
    except:
        return Response(data={"ERROR":query_sql}, status=206)
    pager = int(data["page"]) if "page" in data.keys() else 1
    p = Paginator(_objs, 10)
    all_counts = p.count  # 对象总数
    page_count = p.num_pages  # 总页数
    pj = p.page(pager)
    objs = pj.object_list

    return Response(
        {"search_params": data, "res": objs, "page_count": page_count, "pager": pager, "all_counts": all_counts})



### 访问日志
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def jls_search(request):
    data = request.data
    instance = dict(
        request_method=data["request_method"] if "request_method" in data.keys() else None,
        request_version=data["request_version"] if "request_version" in data.keys() else None,
        src_host=data["src_host"] if "src_host" in data.keys() else None,
        src_ip=data["src_ip"] if "src_ip" in data.keys() else None,
        request_url=data["request_url"] if "request_url" in data.keys() else None,
        category=data["category"] if "category" in data.keys() else None,  # 分类
        content_type=data["content_type"] if "content_type" in data.keys() else None,
        resp_code=int(data["resp_code"]) if "resp_code" in data.keys() else None,
        limit=int(data["limit"]) if "limit" in data.keys() else 100,
        start_time=data["start_time"] if "start_time" in data.keys() else None,
        end_time=data["end_time"] if "end_time" in data.keys() else None,
    )

    from ..utils.seclog_search import seclog_search2
    _objs = from_sql_get_data(seclog_search2(**instance))["data"]
    # return Response(_objs)
    ### 开始准备分页

    pager = int(data["page"]) if "page" in data.keys() else 1
    p = Paginator(_objs, 10)
    all_counts = p.count  # 对象总数
    page_count = p.num_pages  # 总页数
    pj = p.page(pager)
    objs = pj.object_list

    return Response(
        {"search_params": data, "res": objs, "page_count": page_count, "pager": pager, "all_counts": all_counts})
