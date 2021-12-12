from flask import Flask, render_template, g, flash, url_for, request
from flask_cors import CORS
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config

from webapp.analysis.analysis import analysis
from webapp.view.view import view
from webapp.edit.edit import edit

# Конфигурация
DEBUG = True

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

app.register_blueprint(view, url_prefix='/view')
app.register_blueprint(edit, url_prefix='/edit')
app.register_blueprint(analysis, url_prefix="/analysis")

db = SQLAlchemy(app)

from webapp.DBHandler import DBHandler


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def main_page_render():
    tables = DBHandler.get_tables()
    table_menu = [name[1] for name in tables[1:len(tables)]]
    return render_template("_base.html",
                           table_menu=table_menu,
                           module_name=request.endpoint)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        name_table = request.form.get('name_table')
        is_successfully = dbase.update_data(name_table=name_table)
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
        period = request.form.get('sort_analysis')

        return redirect(url_for('analysis.analysis_result_page_render',
                                start_date=start_date,
                                end_date=end_date,
                                period=period))
