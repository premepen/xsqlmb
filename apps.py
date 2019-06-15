
try:
    from django.apps import AppConfig
except:
    AppConfig = object


class LocalAppConfig(AppConfig):
    name = 'xsqlmb'
