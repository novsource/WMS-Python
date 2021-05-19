from webapp.DBHandler import DBHandler
import sqlite3 as sq
import os
from flask import Flask, render_template, g, flash, url_for, request
from werkzeug.utils import redirect

from webapp.analysis.analysis import analysis
from webapp.view.view import view
from webapp.edit.edit import edit

# Конфигурация
DATABASE = 'webapp/WMS.db'
DEBUG = True
SECRET_KEY = "tevirp12as"

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET KEY'] = 'tevirp12'

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'WMS.db')))

app.register_blueprint(view, url_prefix='/view')
app.register_blueprint(edit, url_prefix='/edit')
app.register_blueprint(analysis, url_prefix="/analysis")


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
    tables = dbase.get_tables()
    table_menu = [name[1] for name in tables[1:len(tables)]]
    return render_template("_base.html",
                           table_menu=table_menu,
                           module_name=request.endpoint)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        name_table = request.form.get('name_table')
        is_successfully = dbase.update_data(name_table)
        if is_successfully:
            flash("Редактирование прошло успешно!")
        else:
            flash("Ошибка записи!")
        return redirect(url_for('edit.edit_page_render', name_table=name_table))


@app.route('/analysis_period', methods=['GET', 'POST'])
def analysis_per():
    if request.method == 'POST':
        start_date = request.form.get('analysis_start_date')
        end_date = request.form.get('analysis_end_date')
        return redirect(url_for('analysis.analysis_result_page_render',
                                start_date=start_date,
                                end_date=end_date))
