import math
import sqlite3

from flask import Blueprint, render_template, g, request

from webapp.DBHandler import DBHandler

view = Blueprint('view', __name__, template_folder='templates', static_folder='static')

db = None


@view.before_request
def before_request():
    global db
    db = g.get('link_db')


@view.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@view.route('/<name_table>/', methods=['GET', 'POST'])
def page_render(name_table="undefined"):

    page = int(request.args.get('page', 1))
    links = []

    headers = []

    data = []

    if db:
        try:
            dbase = DBHandler(db)
            if name_table != "table_min_max":
                data = dbase.get_data_from_table(name_table)
            else:
                data = dbase.view_min_max_items()
                name_table = "Минимумы и максимумы хранимого товара"

            headers = data['headers']
            data = data['data']

            for i in range(math.ceil(len(data) / 10)):
                links.append(i)

            links = links[:2] + links[page - 1: page + 1] + links[-2:]

            unique_links = []
            for l in links:
                if l not in unique_links:
                    unique_links.append(l)
            links = unique_links
            data = data[(page - 1) * 10:page * 10]

        except sqlite3.Error as e:
            print('Ошибка чтения данных из БД: ' + str(e))

    return render_template('view_table.html',
                           module_name="Просмотр",
                           name_table=name_table,
                           headers=headers,
                           data=data,
                           links=links)
