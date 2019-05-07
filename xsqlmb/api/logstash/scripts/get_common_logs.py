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

class TxTCommonLog():
    def __init__(self, filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = "/opt/log/waf_log/modsec_audit.log"

    def get_auditlogs(self):
        lines = []
        with open(self.filename, "rb") as f:
            temp_lines = f.readlines()
            for line in temp_lines:
                try:
                    matched = re.match(SysLogFilterParten + "(.*)", line.decode("utf-8") )
                    if matched:
                        # lines.append(matched.group(1))
                        # 2019-5-2 syslog-ng发送切记这里是 2
                        lines.append(matched.group(2) + "\n")
                except:
                    pass
            f.close()
        res = []
        partern = "---(.*?)---(.*?)--.*"
        middle_content = ""
        temp_auditlog_id, temp_auditlog_signal, temp_auditlog_startline, auditlog_endline = "","","",""
        for line_index in range(len(lines)):
            data = re.match(partern, lines[line_index])
            if data:

                if(middle_content == ""):
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
        # 结束了最后一行要加上自己的内容
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
            _detailed_log_txt = convert_aitemlog_to_wedetailed( audit_logid=key, audit_logid_datas=values )
            if _detailed_log_txt:
                modsec_detailed_logs.append(_detailed_log_txt)

        return modsec_detailed_logs

    def get_access_logs(self):
        lines = []
        with open(self.filename, "rb") as f:
            temp_lines = f.readlines() # 整个文本的所有行
            for line in temp_lines:
                try:
                    matched = re.match(SysLogFilterParten + "(.*)", line.decode("utf-8") )
                    if matched:
                        # lines.append(matched.group(1))
                        lines.append(matched.group(2) + "\n")
                except:
                    pass
            f.close()
        # 先去掉`syslog`的发送日志头标识, 接下来才是常规的流程。
        res = []
        for _line in lines:
            import json
            alog = json.loads(_line)
            ua_dict = get_ua_and_os_from_User_Agent(alog['http_user_agent'])
            _temp = dict(alog, **ua_dict)
            res.append(_temp)
            #print(_temp)
        return res, len(temp_lines)

