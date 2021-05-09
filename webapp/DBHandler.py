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
