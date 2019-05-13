# coding=utf-8
# import os
# import datetime
# import logging.config
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# LOG_DIR = os.path.join(BASE_DIR, "_logs")
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)  # 创建路径
#
# LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
#
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "simple": {
#             'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
#         },
#         'standard': {
#             'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
#         },
#     },
#
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "level": "DEBUG",
#             "formatter": "simple",
#             "stream": "ext://sys.stdout"
#         },
#
#         "default": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "level": "INFO",
#             "formatter": "simple",
#             "filename": os.path.join(LOG_DIR, LOG_FILE),
#             'mode': 'w+',
#             "maxBytes": 1024*1024*5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8"
#         },
#     },
#
#     # "loggers": {
#     #     "app_name": {
#     #         "level": "INFO",
#     #         "handlers": ["console"],
#     #         "propagate": "no"
#     #     }
#     # },
#
#     "root": {
#         'handlers': ['default'],
#         'level': "INFO",
#         'propagate': False
#     }
# }
#
# logging.config.dictConfig(LOGGING)
#
import logging as _logging
from fluent import handler

from xsqlmb.settings import LoggerSettings

custom_format = {
  'host': '%(hostname)s',
  'where': '%(module)s.%(funcName)s',  #具体到文件、函数
  'type': '%(levelname)s',
  'stack_trace': '%(exc_text)s'
}

_logging.basicConfig(level=_logging.DEBUG)
logging = _logging.getLogger('fluent.test')
h = handler.FluentHandler('mongo.logger', **LoggerSettings)
formatter = handler.FluentRecordFormatter(custom_format)
h.setFormatter(formatter)
logging.addHandler(h)