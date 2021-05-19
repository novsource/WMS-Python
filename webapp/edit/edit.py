from flask import Blueprint, render_template, g, request, flash, url_for
import sqlite3
import math

from webapp.DBHandler import DBHandler

edit = Blueprint('edit', __name__, template_folder="templates", static_folder="static")

db = None


@edit.before_request
def before_request():
    global db
    db = g.get('link_db')


@edit.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@edit.route('/<name_table>/', methods=['GET', 'POST'])
def edit_page_render(name_table='undefined'):
    page = int(request.args.get('page', 1))
    links = []

    headers = []

    data = []

    if db:
        try:
            dbase = DBHandler(db)
            if name_table != 'table_min_max':
                data = dbase.get_data_from_table(name_table)
            else:
                data = dbase.view_min_max_items()

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

    return render_template('edit_table.html',
                           module_name="Редактирование",
                           name_table=name_table,
                           headers=headers,
                           data=data,
                           data_len=len(data),
                           links=links,
                           count=0)
