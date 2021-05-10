import this

from flask import request


class DBHandler:

    headers = []

    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def get_tables(self):
        sql = '''SELECT * FROM sqlite_master WHERE type="table"'''
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            self.headers = [description[0] for description in self.__cursor.description]
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

                self.headers = [description[0] for description in self.__cursor.description]

                self.__db.commit()
                return True
        except:
            print('Ошибка записи в БД')
        return False

    def get_data_from_table(self, name_table):
        sql = f'''SELECT * FROM {name_table}'''
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            self.headers = [description[0] for description in self.__cursor.description]
            if res:
                return res
        except:
            print('Ошибка получения данных из БД')
            return []

    def view_min_max_items(self):
        try:
            sql = "SELECT item_name, manufacturer_name, shop.shop_address, item_min_count, item_max_count, Item_Storage.item_count " \
                  "FROM Criteria" \
                  " JOIN Items ON Criteria.item_id=Items.item_id" \
                  " JOIN Manufacturer ON Criteria.manufacturer_id=Manufacturer.manufacturer_id" \
                  " JOIN Shop ON Criteria.storage_id=Shop.storage_id" \
                  " JOIN Item_Storage ON Criteria.item_id=Item_Storage.item_id " \
                  "AND Criteria.manufacturer_id=Item_Storage.manufacturer_id " \
                  "AND Criteria.storage_id=Item_Storage.storage_id"

            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()

            self.headers = [description[0] for description in self.__cursor.description]

            if res:
                return res
        except:
            print("Ошибка чтения из БД")
            return []