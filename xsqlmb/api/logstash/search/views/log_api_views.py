# coding:utf-8

from django.core.paginator import Paginator

# from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


from .....src.ltool.sqlconn import from_sql_get_data
from ..utils.access_search import accsslog_search2
from ..utils.seclog_search import seclog_search2

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def accsslog_search(request):
    data = request.data

    instance = dict(
        request_method= data["request_method"] if "request_method" in data.keys() else None,
        request_version=data["request_version"] if "request_version" in data.keys() else None,
        remote_addr=data["remote_addr"] if "remote_addr" in data.keys() else None,
        remote_user=data["remote_user"] if "remote_user" in data.keys() else None,
        server_port=data["server_port"] if "server_port" in data.keys() else None,
        request_url=data["request_url"] if "request_url" in data.keys() else None,
        device=data["device"] if "device" in data.keys() else None,
        os=data["os"] if "os" in data.keys() else None,
        user_agent=data["user_agent"] if "user_agent" in data.keys() else None,
        status=data["status"] if "status" in data.keys() else None,
        body_bytes_sent=data["body_bytes_sent"] if "body_bytes_sent" in data.keys() else None,
        limit= int(data["limit"]) if "limit" in data.keys() else 100,
        is_ignore_static=data["is_ignore_static"] if "is_ignore_static" in data.keys() else True,
        limit_static=data["limit_static"] if "limit_static" in data.keys() else False,
        start_time=data["start_time"] if "start_time" in data.keys() else None,
        end_time=data["end_time"] if "end_time" in data.keys() else None,
        orderby_dt=data["orderby_dt"] if "orderby_dt" in data.keys() else True,
    )
    _sql = accsslog_search2(**instance)
    try:
        _objs = from_sql_get_data(_sql)["data"]
    except:
        return Response(data={"SQL_ERROR": _sql}, status=206)
    # return Response(_objs)
    ## 原来的版本就是直接获取的 _objs
    pager = int(data["page"]) if "page" in data.keys() else 1
    p = Paginator(_objs, 10)
    all_counts = p.count  # 对象总数
    page_count = p.num_pages  # 总页数
    pj = p.page(pager)
    objs = pj.object_list

    return Response(
        {"search_params": data, "res": objs, "page_count": page_count, "pager": pager, "all_counts": all_counts})


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def seclog_search(request):
    data = request.data
    instance = dict(
        server_port=data["server_port"] if "server_port" in data.keys() else None,
        request_method=data["request_method"] if "request_method" in data.keys() else None,
        request_version=data["request_version"] if "request_version" in data.keys() else None,
        #src_host=data["src_host"] if "src_host" in data.keys() else None,
        src_host=None,
        src_ip=data["src_ip"] if "src_ip" in data.keys() else None,
        request_url=data["request_url"] if "request_url" in data.keys() else None,
        category=data["category"] if "category" in data.keys() else None, # 分类
        content_type=data["content_type"] if "content_type" in data.keys() else None,
        resp_code=int(data["resp_code"]) if "resp_code" in data.keys() else None,
        limit=int(data["limit"]) if "limit" in data.keys() else 100,
        start_time=data["start_time"] if "start_time" in data.keys() else None,
        end_time=data["end_time"] if "end_time" in data.keys() else None,
    )
    _sql = seclog_search2(**instance)
    try:
        _objs = from_sql_get_data(_sql)["data"]
    except:
        return Response({"SQL_ERROR":_sql})
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



# from phaser1.models import ApacheAccessLogDetail
# class AcccesLogSearchViewSet(viewsets.ViewSet):
#     def get_queryset(self):
#         user = self.request.user
#         return user
#
#     queryset = []
#     serializer_class = AccesslogSearchSerializer
#
#
# accs_router = routers.DefaultRouter()
# accs_router.register(r'accesslog_search', AcccesLogSearchViewSet)

