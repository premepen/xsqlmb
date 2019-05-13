from xsqlmb.src.ltool.sqlconn import from_sql_get_data


def get_waf_access_log_columns(reject_list=("id", "remote_user")):
    datas = from_sql_get_data("desc waf_access_log")["data"]
    fields = [x['Field'] for x in datas]
    for key in reject_list:
        try:
            fields.remove(key)
        except:
            pass
    return fields


def get_waf_alert_log_columns(reject_list=("id", )):
    datas = from_sql_get_data("desc waf_alert_log")["data"]
    fields = [x['Field'] for x in datas]
    for key in reject_list:
        try:
            fields.remove(key)
        except:
            pass
    return fields
    #return "`" + "`, `".join(fields) + "`"