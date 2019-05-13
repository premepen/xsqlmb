# coding:utf-8
import re
from datetime import datetime

from xsqlmb.api.logstash.utils.dt_tool import get_pydt_based_logdt
from xsqlmb.src.ltool.utils.dt_tool import re_upgrade_str


## 审计日志头
def modsec_Alog_extract(content_str):
    matched1 = re.match("\[(.*?) \+0[8|0]00\] (\d+\.\d+) (.*?) (\d+) (.*?) (\d+).*?", content_str.replace("\n", "") )
    ## 这个位置谨防告警日期格式存在其他情况; 后续再增加正则匹配
    if matched1:
        res = dict(
            audit_time = get_pydt_based_logdt(matched1.group(1)),
            uniq_id = matched1.group(2),
            src_ip = matched1.group(3),
            logsize = matched1.group(4),
            src_host = matched1.group(5),
            server_port = matched1.group(6),
        )
        return res
    print("==============1============")
    print(content_str)
    print("==============2============")
    return dict(
        audit_time=str(datetime.now()),
        uniq_id="-",
        src_ip="121.121.121.121",
        logsize=0,
        src_host="-",
        server_port="0",
    )

# request_line 解析
def modsec_Blog_extract(content_str):
    http_user_agent_matd = re.match("([A-Z]+)\s(.*?)(HTTP.*?)\n.*", content_str)
    hua_matd = re.findall(".*?\nUser-Agent: (.*?)\n.*", content_str)

    request_header_infos = {"http_user_agent": ""}
    if hua_matd:
        request_header_infos["http_user_agent"] = hua_matd[0]
    if http_user_agent_matd:
        request_header_infos1 = dict(
            request_method=http_user_agent_matd.group(1),
            request_url=http_user_agent_matd.group(2),
            http_ver = http_user_agent_matd.group(3)
        )
        res = dict(request_header_infos, **request_header_infos1)
        return res
    try:
        from xsqlmb.src.cfgs.logConfig import logging
    except:
        import logging
    logging.warning("B阶段日志处理丢失:" + content_str)
    return dict(
        request_method=http_user_agent_matd.group(1),
        request_url="__waf_sensitive_url_partern__",
        http_ver="http/1.1"
    )

## 响应信息
def modsec_Flog_extract(content_str):
    response_header_infos = dict(
        http_ver="http/0.9",
        resp_code="403",
        waf_serv="tengine-v2.0.3",
        content_type="text/html",
        content_length="0",
    )
    matd1 = re.match(".*?(HTTP.*?)\s(\d+)\n", content_str)
    matd2 = re.findall(".*?Server:\s(.*?)\n", content_str)
    matd3 = re.findall(".*?Content-Type:\s(.*?)\n", content_str)
    matd4 = re.findall(".*?Content-Length:\s(\d+)\n", content_str)
    if matd1:
        response_header_infos["http_ver"] = matd1.group(1)
        response_header_infos["resp_code"] = matd1.group(2)
    if matd2:
        response_header_infos["waf_serv"] = matd2[0]
    if matd3:
        response_header_infos["content_type"] = matd3[0]
    if matd4:
        response_header_infos["content_length"] = matd4[0]

    return response_header_infos


### H 阶段的 Log 函数；服务于后面的所有
def modsec_Hlog_extract(frstr):
    SPLIT_KEY = "JtsdWwdzZbx"
    new_str = frstr.replace("ModSecurity: ", SPLIT_KEY + "ModSecurity: ")
    res_dict_array = []

    _count_cate = {}

    for x in new_str.split(SPLIT_KEY):
        if "ModSecurity" in x:
            prefix_partern = re.match("(ModSecurity: .*)\[file.*", x).group(1)
            prefix_len = len(prefix_partern)
            features = re.findall("""\[(\w+)\s"(.*?)"\]""", x[prefix_len:])
            alert_dct = {}
            alert_dct.setdefault("tag", [])

            for (key, value) in features:
                if key == "tag":
                    alert_dct[key].append(value)
                    continue
                alert_dct.setdefault(key, value)
            # res_dict_array.append(alert_dct)

            try:
                _file = alert_dct["file"]
            except:
                _file = ""

            # 2019-5-1 修改; 通过规则的文件名来定位规则的类型 ====
            from xsqlmb.src.ltool.rules.rulecate import get_rule_cate_by_filepath
            _category = get_rule_cate_by_filepath(_file)
            if _category in _count_cate.keys():
                _count_cate[_category] += 1
            else:
                _count_cate.setdefault(_category, 1)
            # 2019-5-1 ========================================
            res_dict_array.append(dict(
                rule_id = alert_dct["id"],
                matched_data = alert_dct["data"] if "data" in alert_dct.keys() else "",
                msg = alert_dct["msg"] if "msg" in alert_dct.keys() else "",
                file = _file,
                _category = _category,
            ))
    try:
        res_data = sorted(_count_cate.items(), key=lambda x: _count_cate[x[0]], reverse=True)[0]
        category = res_data[0]
    except:
        try:
            category = [x["_category"] for x in res_dict_array][0]
        except:
            category = "自定义规则2"
    try:
        alert_msg = [x["msg"] for x in res_dict_array][0]
    except:
        alert_msg = "自定义过滤2"
    # 2019-5-1 在这个层面增加了日志的message
    return {"hloginfo": res_dict_array, "category": category, "msg": alert_msg}


def having_write2file(audit_logid):
    """
    2019-5-6 写入本地文件的校验。
    将告警日志的条目全部写入到本地文件。
    :param audit_logid:
    :return: 告警日志的ID
    """
    import os
    from xsqlmb.api.logstash.cfgs.configs import PcapDir
    game_dir_path = os.path.join(PcapDir, audit_logid + ".txt")
    if os.path.exists(game_dir_path):
        return None
    else:
        return game_dir_path

def having_saved2db(audit_logid):
    """
    2019-5-7 写入mysql数据库的校验
    将告警日志的条目全部写入到本地文件。
    :param audit_logid: 告警日志的ID
    :return: 返回是否存在
    """
    import os
    from xsqlmb.api.logstash.cfgs.configs import PcapDir
    game_dir_path = os.path.join(PcapDir, audit_logid + ".txt")
    if os.path.exists(game_dir_path):
        return None
    else:
        return game_dir_path


def convert_aitemlog_to_wedetailed(audit_logid, audit_logid_datas=None):
    """
    根据日志产生的 audit_logid 获取到所有的日志信息
    :param audit_logid:
    :param audit_logid_datas:
    :return:
    """
    _audit_extract_log = having_write2file(audit_logid)
    if not _audit_extract_log:
        return None

    temp = {"audit_logid": audit_logid}
    for x in audit_logid_datas:
        # exec("""temp = dict(temp, **modsec_"""+ x["auditlog_signal"] +"""log_extract(x["auditlog_content"]))""")
        if x["auditlog_signal"] == "A":
            temp = dict(temp, **modsec_Alog_extract(x["auditlog_content"]))
        if x["auditlog_signal"] == "B":
            temp = dict(temp, **modsec_Blog_extract(x["auditlog_content"]))
        if x["auditlog_signal"] == "F":
            temp = dict(temp, **modsec_Flog_extract(x["auditlog_content"]))
        if x["auditlog_signal"] == "H":
            temp = dict(temp, **modsec_Hlog_extract(x["auditlog_content"]))
    try:
        return temp
    finally:
        from xsqlmb.src.ltool.utils.filemg_util import file_lock_write
        file_lock_write(str(temp), _audit_extract_log)


def convert_auditlog_detaild(audit_logid, audit_logid_datas=None):
    """
    根据日志产生的 audit_logid 获取到所有的日志信息
    :param audit_logid:
    :param audit_logid_datas:
    :return:
    """
    temp = {"audit_logid": audit_logid}
    try:
        alog, blog, flog, hlog = False, False, False, False
        for x in audit_logid_datas:
            # exec("""temp = dict(temp, **modsec_"""+ x["auditlog_signal"] +"""log_extract(x["auditlog_content"]))""")
            if x["auditlog_signal"] == "A":
                temp = dict(temp, **modsec_Alog_extract(re_upgrade_str(x["auditlog_content"])))
                alog = True
            if x["auditlog_signal"] == "B":
                temp = dict(temp, **modsec_Blog_extract(re_upgrade_str(x["auditlog_content"])))
                blog = True
            if x["auditlog_signal"] == "F":
                temp = dict(temp, **modsec_Flog_extract(re_upgrade_str(x["auditlog_content"])))
                flog = True
            if x["auditlog_signal"] == "H":
                temp = dict(temp, **modsec_Hlog_extract(re_upgrade_str(x["auditlog_content"])))
                hlog = True
        if not hlog:
            temp = dict(temp, **dict(msg="Sensitive Url Payload Alert.", category="异常捕获"))

        if alog and blog and flog:
            return temp
    except:
        from xsqlmb.api.logstash.scripts.txt.get_common_logs import logging
        logging.error("extract告警日志错误！" + str(audit_logid))
        return None




