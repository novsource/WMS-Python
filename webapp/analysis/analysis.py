import sqlite3
import math

from flask import Flask, Blueprint, render_template, request, g, url_for

from webapp.DBHandler import DBHandler

analysis = Blueprint('analysis', __name__, template_folder='templates', static_folder='static')

db = None


@analysis.before_request
def before_request():
    global db
    db = g.get('link_db')


@analysis.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@analysis.route('/result/<start_date>/<end_date>', methods=['GET', 'POST'])
def analysis_result_page_render(start_date="Undefined", end_date="Undefined"):
    page = int(request.args.get('page', 1))
    links = []

    if db:
        dbase = DBHandler(db)
        data = dbase.get_info_about_sell_from_period(start_date=start_date, end_date=end_date)

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

    return render_template('analysis_date.html',
                           module_name="Результаты анализа",
                           data=data,
                           headers=headers,
                           start_date=start_date,
                           end_date=end_date,
                           links=links)

def count_