try:
    from django.apps import AppConfig
except:
    AppConfig = object


class Phaser2Config(AppConfig):
    name = 'xsqlmb'
