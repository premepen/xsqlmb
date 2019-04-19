from xsqlmb.src.cfgs.basicConfig import DATABASES


class XdbManager():

    def __init__(self):
        self.db_name = DATABASES["default"]["NAME"]

    @staticmethod
    def _create():
        from xsqlmb.src.ltool.sqlconn import sql_action
        sql_action("""CREATE DATABASE {db_name} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;""".format(db_name=DATABASES["default"]["NAME"]))
        return True