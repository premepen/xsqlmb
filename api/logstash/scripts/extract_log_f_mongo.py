# coding:utf-8
import re

# from utils.mongo import MongoConn
from xsqlmb.api.logstash.utils.dt_tool import get_ua_and_os_from_User_Agent
from xsqlmb.api.logstash.opt.wt_parse import convert_aitemlog_to_wedetailed, convert_auditlog_detaild
from xsqlmb.api.logstash.cfgs.configs import SysLogFilterParten

try:
    from xsqlmb.src.cfgs.logConfig import logging
except:
    import logging

# MPConn = MongoConn(SysLogMongoDBConfig)
from xsqlmb.src.ltool.mongo import MongoConn


class ExtractLogFromMongo():
    def __init__(self, table_name="waf_alert_log"):
        self.table_name = table_name

    def get_auditlogs(self):
        lines = []

        _datas = MongoConn().query_timestamp_datas(table_name=self.table_name)
        if not _datas:
            return []
        for data in _datas:
            lines.append(data["message"] + "\n")


        res = []
        partern = "---(.*?)---(.*?)--.*"
        middle_content = ""
        temp_auditlog_id, temp_auditlog_signal, temp_auditlog_startline, auditlog_endline = "","","",""
        for line_index in range(len(lines)):
            data = re.match(partern, lines[line_index])
            if data:

                if(middle_content in ["", "\n"] ):
                    # 第一次进来了但是已经收集了中间的数据
                    temp_auditlog_id = data.group(1)
                    temp_auditlog_signal = data.group(2)
                    temp_auditlog_startline = line_index
                else:
                    # 第二次进来了但是已经收集了中间的数据
                    temp_auditlog_endline = line_index - 1
                    res.append(dict(
                        audit_logid=temp_auditlog_id,
                        auditlog_signal=temp_auditlog_signal,
                        auditlog_startline=temp_auditlog_startline,
                        auditlog_endline=temp_auditlog_endline,
                        auditlog_content=middle_content,
                        ))
                    # 收集完了就把这个中间内容集合置为空
                    middle_content = ""
                    data = re.match(partern, lines[line_index])
                    temp_auditlog_id = data.group(1)
                    temp_auditlog_signal = data.group(2)
                    temp_auditlog_startline = line_index
                continue

            middle_content += lines[line_index]
        # 切记这里异常捕获的结果中如果 audit_logid 不满足我们的条件应该删除。
        if temp_auditlog_id != "":
            res.append(dict(
                audit_logid=temp_auditlog_id,
                auditlog_signal=temp_auditlog_signal,
                auditlog_startline=temp_auditlog_startline,
                auditlog_endline=temp_auditlog_startline,
                auditlog_content="",
            ))
        return res

    def modseclog_to_detaild(self):
        modsec_txtlogs = self.get_auditlogs()
        ## 建立一个键值队的集合，一个键key（audit_logid） 对应一个关于它自己的列表
        _modsec_txtlog_dict = {}
        for x in modsec_txtlogs:
            if "audit_logid" in x.keys():
                if x["audit_logid"] in _modsec_txtlog_dict.keys():
                    _modsec_txtlog_dict[x["audit_logid"]].append(x)
                else:
                    ## 注意这里是把这个audit_logid作为字符串的键值对的`键`
                    _modsec_txtlog_dict[x["audit_logid"]] = [x]
            else:
                logging.debug("ERROR-NO-AuditLogId!")
        modsec_detailed_logs = []
        for key, values in _modsec_txtlog_dict.items():
            #_detailed_log_txt = convert_aitemlog_to_wedetailed( audit_logid=key, audit_logid_datas=values )
            _detailed_log_txt = convert_auditlog_detaild( audit_logid=key, audit_logid_datas=values )
            if _detailed_log_txt:
                modsec_detailed_logs.append(_detailed_log_txt)
        return modsec_detailed_logs

    def get_access_logs(self):
        lines = []
        _datas = MongoConn().query_timestamp_datas(table_name=self.table_name)
        if not _datas:
            return [], 0
        for data in _datas:
            lines.append(data["message"])

        # 先去掉`syslog`的发送日志头标识, 接下来才是常规的流程。
        res = []
        for _line in lines:
            import json
            alog = json.loads(_line.replace('\\', "\\\\"), encoding="utf-8")

            ua_dict = get_ua_and_os_from_User_Agent(alog['http_user_agent'])
            _temp = dict(alog, **ua_dict)

            res.append(_temp)

        return res, len(_datas)

