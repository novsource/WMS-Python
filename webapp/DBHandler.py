from flask import request


class DBHandler:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getTables(self):
        sql = '''SELECT * FROM sqlite_master WHERE type="table"'''
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except:
            print('Ошибка чтения из БД')
        return []

    def update_data(self, name_table):
        try:
            if name_table == 'Items':
                item_id = int(request.form.get("item_id"))
                item_name = request.form.get("item_name")
                item_cost = float(request.form.get("item_cost"))

                sql = f'''UPDATE {name_table} SET(item_name, item_cost) = ("{item_name}", {item_cost})''' \
                      + f''' WHERE item_id={item_id}'''

                self.__cursor.execute(sql)
                self.__db.commit()
                return True
        except:
            print('Ошибка записи в БД')
        return False
