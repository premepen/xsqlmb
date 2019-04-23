
class MutiTypesInsets2SqlClass():

    def __init__(self, table_name):
        """
        支持多种类型的字符串进行写入到mysql
        :param table_name: 表格名称
        """
        self.table_name = table_name


    def filetype2sql(self, filepath):
        pass


    def arrays2sql(self, array2, columns_order):
        """
        数组对象导入到mysql
        :param array2: 数组就是 Insert into 后面 values ({}) 这个对象
        :param columns_order: 就是 insert into table({``,``}) 里面的对象。
        :return:
        """
        if len(array2) < 1:
            return False, "数据不足插入"
        if len(array2[0]) != len(columns_order):
            return False, "带插入对象数据列不匹配"

        _sql_str_list = []
        for _item in array2:
            _sql_str = "(\'" + "\',\'".join(_item) + "\')"
            _sql_str_list.append(_sql_str)
        _query_sql = """insert into {table_name}({columns}) values {values_str};""".format(
            values_str=", ".join([str(x) for x in _sql_str_list]),
            table_name=self.table_name,
            columns=columns_order
        )
        try:
            from  xsqlmb.src.ltool.sqlconn import sql_action
            sql_action(_query_sql)
        except:
            try:
                from  xsqlmb.src.cfgs.logConfig import logging
            except:
                import logging
            logging.info("导入数据库失败！")
