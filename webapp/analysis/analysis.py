import datetime
import math

from flask import Flask, Blueprint, render_template, request, g, url_for, redirect

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


@analysis.route('/result/<start_date>/<end_date>/<period>', methods=['GET', 'POST'])
def analysis_result_page_render(start_date="Undefined", end_date="Undefined", period="Undefined"):
    page = int(request.args.get('page', 1))
    links = []

    if db:
        dbase = DBHandler(db)

        data = dbase.get_info_about_sell_from_period(start_date, end_date)

        data = data['data']

        result_analysis = analysis_sell(data, start_date, end_date, period)
        new_data = create_new_min_max(result_analysis)

        headers = dbase.view_min_max_items()['headers']

        for i in range(math.ceil(len(new_data) / 10)):
            links.append(i)

        links = links[:2] + links[page - 1: page + 1] + links[-2:]

        unique_links = []
        for l in links:
            if l not in unique_links:
                unique_links.append(l)
        links = unique_links
        new_data = new_data[(page - 1) * 10:page * 10]

        dbase.update_min_max()

    return render_template('analysis_date.html',
                           module_name="Результаты анализа",
                           data=new_data,
                           headers=headers,
                           start_date=start_date,
                           end_date=end_date,
                           links=links)


def count_sell_item(data, start_date, end_date, period):
    count_start_date = {}
    count_end_date = {}
    period = get_period(period=period)

    for sell in data:
        date = datetime.datetime.strptime(sell[3].split(" ")[0], "%Y-%m-%d")
        razn = int((datetime.datetime.strptime(start_date, "%Y-%m-%d") - date).days)
        if razn < period:
            if count_start_date.get(sell[0]) is not None:
                count_start_date[sell[0]] += sell[6] * sell[7]
            else:
                count_start_date[sell[0]] = sell[6] * sell[7]
        razn = int(((datetime.datetime.strptime(end_date, "%Y-%m-%d")) - date).days)
        if razn < period:
            if count_end_date.get(sell[0]) is not None:
                count_end_date[sell[0]] += sell[6] * sell[7]
            else:
                count_end_date[sell[0]] = sell[6] * sell[7]

    count = {start_date: count_start_date, end_date: count_end_date}

    return count


def analysis_sell(data, start_date, end_date, period):
    count = count_sell_item(data, start_date, end_date, period)
    result_analysis = {}
    for i in range(len(count[start_date].values())):
        key = list(count[start_date].keys())[i]
        result = int((count[start_date].get(key) - count[end_date].get(key)) / count[start_date].get(key)) * 100
        result_analysis[key] = result
    return result_analysis


def get_period(period):
    days_in_period = {
        "week": 7,
        "month": 31
    }[period]
    return days_in_period


def create_new_min_max_from_db(new_min_max_dict):
    dbase = DBHandler(db)
    old_data = dbase.view_min_max_items()['data']
    old_data = [list(turp) for turp in old_data]
    for i in range(len(new_min_max_dict.values())):
        key = list(new_min_max_dict.keys())[i]
        if new_min_max_dict.get(key) < -15:
            old_data[i][4] += int(old_data[i][4] * 0.2)
            old_data[i][5] += int(old_data[i][5] * 0.2)
        if (new_min_max_dict.get(key) <= -5) and (new_min_max_dict.get(key) >= -15):
            old_data[i][4] += int(old_data[i][4] * 0.1)
            old_data[i][5] += int(old_data[i][5] * 0.1)
        if (new_min_max_dict.get(key) >= 5) and (new_min_max_dict.get(key) <= 15):
            old_data[i][4] -= int(old_data[i][4] * 0.1)
            old_data[i][5] -= int(old_data[i][5] * 0.1)
        if new_min_max_dict.get(key) > 15:
            old_data[i][4] -= int(old_data[i][4] * 0.2)
            old_data[i][5] -= int(old_data[i][5] * 0.2)
    dbase.write_data_into_local_db("analysis_res", data=old_data)
    return old_data


def create_new_min_max_with_data(new_min_max_dict, data):
    old_data = data
    for i in range(len(new_min_max_dict.values())):
        key = list(new_min_max_dict.keys())[i]
        if new_min_max_dict.get(key) < -15:
            old_data[i][4] += int(old_data[i][4] * 0.2)
            old_data[i][5] += int(old_data[i][5] * 0.2)
        if (new_min_max_dict.get(key) <= -5) and (new_min_max_dict.get(key) >= -15):
            old_data[i][4] += int(old_data[i][4] * 0.1)
            old_data[i][5] += int(old_data[i][5] * 0.1)
        if (new_min_max_dict.get(key) >= 5) and (new_min_max_dict.get(key) <= 15):
            old_data[i][4] -= int(old_data[i][4] * 0.1)
            old_data[i][5] -= int(old_data[i][5] * 0.1)
        if new_min_max_dict.get(key) > 15:
            old_data[i][4] -= int(old_data[i][4] * 0.2)
            old_data[i][5] -= int(old_data[i][5] * 0.2)
    return old_data

@analysis.route('/result/')
def analysis_complete():
    if request.method == "POST":
        print("Hello")
    return redirect(url_for('view.view_page_render', name_table='table_min_max'))
