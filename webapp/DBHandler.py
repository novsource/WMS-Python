import datetime
from flask import request


class DBHandler:
    data_from_db = {}

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
            if name_table == 'table_min_max':
                item_id = int(request.form.get("item_id"))
                item_name = request.form.get("item_name")
                item_cost = float(request.form.get("item_cost"))

                sql = f'''UPDATE {name_table} SET(item_name, item_cost) = ("{item_name}", {item_cost})''' \
                      + f''' WHERE item_id={item_id}'''

                self.__cursor.execute(sql)

                self.__db.commit()
                return True
        except:
            print('Ошибка обновления записи в БД')
            return False

    def get_data_from_table(self, name_table):
        sql = f'''SELECT * FROM {name_table}'''
        try:
            if self.data_from_db.get(name_table) is None:
                self.__cursor.execute(sql)
                res = self.__cursor.fetchall()

                headers = [description[0] for description in self.__cursor.description]

                if res:
                    self.data_from_db[name_table] = {"headers": headers, "data": res}
                    return self.data_from_db.get(name_table)
            else:
                return self.data_from_db.get(name_table)
        except:
            print('Ошибка получения данных из БД')
            return []

    def view_min_max_items(self):
        try:
            name_table = 'Минимумы и максимумы хранимого товара'
            sql = "SELECT criteria_id, item_name, manufacturer_name, shop.shop_address, item_min_count, item_max_count, Item_Storage.item_count " \
                      "FROM Criteria" \
                      " JOIN Items ON Criteria.item_id=Items.item_id" \
                      " JOIN Manufacturer ON Criteria.manufacturer_id=Manufacturer.manufacturer_id" \
                      " JOIN Shop ON Criteria.storage_id=Shop.storage_id" \
                      " JOIN Item_Storage ON Criteria.item_id=Item_Storage.item_id " \
                      "AND Criteria.manufacturer_id=Item_Storage.manufacturer_id " \
                      "AND Criteria.storage_id=Item_Storage.storage_id"

            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()

            headers = [description[0] for description in self.__cursor.description]

            if res:
                self.data_from_db[name_table] = {"headers": headers, "data": res}
                return self.data_from_db.get(name_table)
        except:
            print("Ошибка чтения из БД")
            return []

    def get_info_about_sell_from_period(self, start_date, end_date):
        sql = f'''SELECT item_storage_id, item_name, manufacturer_name, sell_date, item_min_count, item_max_count, sell_count, item_cost 
                FROM Item_Sell 
                JOIN Items ON Items.item_id = (SELECT item_id FROM Item_Storage WHERE item_storage_id = Item_Sell.item_storage_id)
                JOIN Manufacturer ON Manufacturer.manufacturer_id = (SELECT manufacturer_id FROM Item_Storage WHERE item_storage_id = Item_Sell.item_storage_id)
                JOIN Item_Manufacturer ON (Item_Manufacturer.item_id = (SELECT item_id FROM Item_Storage WHERE item_storage_id = Item_Sell.item_storage_id)) 
					AND (Item_Manufacturer.manufacturer_id = (SELECT manufacturer_id FROM Item_Storage WHERE item_storage_id = Item_Sell.item_storage_id))
                JOIN Criteria ON (Criteria.item_id = (SELECT item_id FROM Item_Storage WHERE item_storage_id = Item_Sell.item_storage_id)) 
					AND (Criteria.manufacturer_id = (SELECT manufacturer_id FROM Item_Storage WHERE item_storage_id = Item_Sell.item_storage_id)) 
                WHERE (strftime('%s', sell_date) BETWEEN strftime('%s', '{start_date}') AND strftime('%s', '{start_date}', '+7 days')) 
	                OR (strftime('%s', sell_date) BETWEEN strftime('%s', '{end_date}') AND strftime('%s', '{end_date}', '+7 days'));'''
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()

            headers = [description[0] for description in self.__cursor.description]

            if res:
                self.data_from_db["analysis"] = {"headers": headers, "data": res}
                return self.data_from_db.get("analysis")
        except:
            print("Error")
            return []

    def update_min_max(self):
        try:
            for row in self.data_from_db['analysis_res']:
                self.__cursor.execute(f"UPDATE Criteria SET(item_min_count, item_max_count) = ({row[4]},{row[5]}) "
                                      f"WHERE criteria_id = {row[0]}")
                self.__db.commit()
        except:
            print("Ошибка записи")
            return []

    def write_data_into_local_db(self, key1, data):
        self.data_from_db[key1] = data

    def get_data_from_local_db(self, key):
        return self.data_from_db.get(key)
