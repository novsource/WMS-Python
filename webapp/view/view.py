import math
import sqlite3

from flask import Blueprint, render_template, g, request

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

    if request.method == "POST":
        print(request.form.getlist('checkbox'))
        return 'Done'

    page = int(request.args.get('page', 1))
    links = []

    data = []
    headers = []

    if db:
        try:
            cur = db.cursor()
            cur.execute(f'''SELECT * FROM {name_table}''')
            data = cur.fetchall()
            headers = [description[0] for description in cur.description]

            for i in range(math.ceil(len(data) / 5)):
                links.append(i)

            links = links[:2] + links[page - 1: page + 1] + links[-2:]

            unique_links = []
            for l in links:
                if l not in unique_links:
                    unique_links.append(l)
            links = unique_links
            data = data[(page - 1) * 5:page * 5]

        except sqlite3.Error as e:
            print('Ошибка чтения данных из БД: ' + str(e))

    return render_template('index.html',
                           name_table=name_table,
                           headers=headers,
                           data=data,
                           links=links)