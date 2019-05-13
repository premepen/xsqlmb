# coding:utf-8

res_pratean = """
REQUEST-903.9001-DRUPAL-EXCLUSION-RULES.conf（规则应用示例）
REQUEST-903.9002-WORDPRESS-EXCLUSION-RULES.conf（规则应用示例）
REQUEST-910-IP-REPUTATION.conf（可疑IP匹配）
REQUEST-911-METHOD-ENFORCEMENT.conf（强制方法）
REQUEST-912-DOS-PROTECTION.conf（DOS攻击）
REQUEST-913-SCANNER-DETECTION.conf（扫描器检测）
REQUEST-920-PROTOCOL-ENFORCEMENT.conf（HTTP协议规范相关规则）
REQUEST-921-PROTOCOL-ATTACK.conf（协议攻击）
- 举例：HTTP Header Injection Attack、HTTP参数污染
REQUEST-930-APPLICATION-ATTACK-LFI.conf（应用攻击-路径遍历）
REQUEST-931-APPLICATION-ATTACK-RFI.conf（远程文件包含）
REQUEST-932-APPLICATION-ATTACK-RCE.conf（远程命令执行）
REQUEST-933-APPLICATION-ATTACK-PHP.conf（PHP注入攻击）
REQUEST-941-APPLICATION-ATTACK-XSS.conf（XSS注入攻击）
REQUEST-942-APPLICATION-ATTACK-SQLI.conf（SQL注入攻击）
REQUEST-943-APPLICATION-ATTACK-SESSION-FIXATION.conf（会话固定）
REQUEST-949-BLOCKING-EVALUATION.conf（引擎上下文联合评估）
RESPONSE-950-DATA-LEAKAGES.conf（信息泄露）
RESPONSE-951-DATA-LEAKAGES-SQL.conf（SQL信息泄露）
RESPONSE-952-DATA-LEAKAGES-JAVA.conf（JAVA源代码泄露）
RESPONSE-953-DATA-LEAKAGES-PHP.conf（PHP信息泄露）
RESPONSE-954-DATA-LEAKAGES-IIS.conf（IIS信息泄露）
REQUEST-905-COMMON-EXCEPTIONS.conf（常见示例）
REQUEST-901-INITIALIZATION.conf（引擎初始化）
modsecurity.conf（引擎内置补丁规则和设置）
localized.conf（自定义规则过滤）
dynamic.conf（自定义规则访问控制）
RESPONSE-980-CORRELATION.conf（内置关联规则）
REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example（引擎规则解释器）
RESPONSE-959-BLOCKING-EVALUATION.conf（引擎上下文联合评估）"""

import re

def get_kv_of_rukes():
    regexp = {}
    for x in res_pratean.split("\n"):
        # matched = re.match(".*?[\-|\.](\d+)\-.*?\.conf（(.*?)）", x)
        matched = re.match("^(.*?\.conf)（(.*?)）", x)
        if matched:
            regexp.setdefault(matched.group(1), matched.group(2))
    return regexp


def get_rule_cate_by_filepath(filepath):
    try:
        filename = filepath.split("/")[-1:][0]
        return get_kv_of_rukes()[filename]
    except:
        return "自定义规则"
