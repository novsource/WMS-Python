# Config для БД

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:LpYTE57C2021@server/Shop?driver=SQL+Server?trusted_connection=yes'
    SQLALCHEMY_TRACK_MODIFICATION = False
