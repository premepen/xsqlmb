import pymysql

try:
    from website.settings import DATABASES
except:
    from xsqlmb.settings import DATABASES


MPP_CONFIG = {
    'host': DATABASES["default"]["HOST"],
    'port': DATABASES["default"]["PORT"],
    'user': DATABASES["default"]["USER"],
    'password': DATABASES["default"]["PASSWORD"],
    'db': DATABASES["default"]["NAME"],
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}


default_engine = "InnoDB"
default_charset = "utf8"
charset_types = ["utf8", "utf32","gbk", "gb2312","binnary", "utf32", "utf16", "utf8mb4"]
engine_types = ["InnoDB", "MyISAM"]


filter_types = ["between", "contains", "regexp", "group"]


