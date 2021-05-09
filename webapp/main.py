from webapp.DBHandler import DBHandler
import sqlite3 as sq
from flask import Flask, render_template, g
import os
from webapp.view.view import view
from webapp.edit.edit import edit

# Конфигурация
DATABASE = 'WMS.db'
DEBUG = True
SECRET_KEY = "tevirp12as"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'WMS.db')))

app.register_blueprint(view, url_prefix='/view')
app.register_blueprint(edit, url_prefix='/edit')


def connector_db():
    conn = sq.connect(app.config['DATABASE'])
    #conn.row_factory = sq.Row
    return conn


def get_db():
    # Коннект к БД если его еще нет
    if not hasattr(g, 'link_db'):
        g.link_db = connector_db()
    return g.link_db


if __name__ == '__main__':
    app.run(debug=True)

dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DBHandler(db)


@app.teardown_appcontext
def close_db(error):
    if not hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def main_page_render():
    tables = dbase.getTables()
    table_menu = [name[1] for name in tables[1:len(tables)]]
    return render_template("_base.html",
                           table_menu=table_menu)