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


@analysis.route('/result')
def analysis_result_page_render():

    return render_template('analysis_date.html',
                           module_name="Результаты анализа")