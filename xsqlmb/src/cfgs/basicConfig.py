import pymysql

try:
    from website.settings import DATABASES
except:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'p3',
            'USER': 'root',
            'PASSWORD': 'test@1q2w2e4R',
            'HOST': "192.168.2.55",
            'PORT': 3306,
        }
    }


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


