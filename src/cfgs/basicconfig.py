import pymysql


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbtest',
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
