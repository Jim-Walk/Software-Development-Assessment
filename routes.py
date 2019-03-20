from flask import Flask, render_template, request, json, redirect, url_for, abort, session
from pymongo import MongoClient

import sys
import random,json,math

from helpers import get_logo, get_wiki, rank_it
from models import SearchClass, Institutions, Courses, RankClass
from copy import deepcopy

from bson.json_util import dumps

client = MongoClient()
db = client.rankit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        query = request.args.get("searchInput")
        #hacky input sanitization
        query = str(query.replace("<",""))
        query = query.replace(">","")

        search_result = SearchClass().GlobalSearch(query)
        return render_template('search_result.html', results=search_result, search_query=query)
    else:
        return redirect(url_for("index"))


@app.route('/institution/<int:UKPRN>')
def institution(UKPRN):
    inst = Institutions().GetByPRN(UKPRN)
    if inst == None: #fail gracefully if the institution is not found
        abort(404)
    logo = get_logo(inst['PROVIDER_NAME'])
    #logo = "https://via.placeholder.com/1200x1200.png?text=InstitutionLogo" #in case you exceed the limit
    wiki = get_wiki(inst['PROVIDER_NAME'])
    courses = Courses()
    top_courses = courses.GetTopPerInstitution(UKPRN)
    all_courses = courses.GetByInstitution(UKPRN)
    return render_template('institution.html', inst=inst, top_courses=top_courses,
                           logo=logo, wiki=wiki, all_courses=all_courses)

@app.route('/course/<int:UKPRN>/<KISCOURSEID>')
def course(UKPRN, KISCOURSEID):
    institution = Institutions().GetByPRN(UKPRN)
    course = Courses().GetSingleByKIS(KISCOURSEID)
    related_courses=Courses().GetRelatedBySubject(KISCOURSEID)
    if course == None:
        abort(404)
    return render_template('course.html', 
                            course=course, 
                            institution=institution,
                            related_courses=related_courses
                           )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/unis')
def unis():
    uni_list = Institutions().GetAll()
    return render_template('uni-list.html', uni_list = uni_list)

@app.route('/rank', methods=['GET', 'POST'])
def rank():
    pref_grad = int(request.form['grad_rates'])
    pref_empl = int(request.form['empl_chance'])
    pref_salary = int(request.form['salary'])
    pref_studfeed = int(request.form['teaching'])
    rank = RankClass(request.form['department'], pref_grad, pref_empl, pref_salary, pref_studfeed)
    outdata = dumps(rank.GetResult())
    response = app.response_class(
        response=json.dumps(outdata),
        mimetype='application/json'
    )
    return response  

@app.route('/rankt')
def rankt():
    pref_grad = 50
    pref_empl = 50
    pref_salary = 50
    pref_studfeed = 50
    rank = RankClass('CAH10', pref_grad, pref_empl, pref_salary, pref_studfeed)
    outdata = dumps(rank.GetResult())
    response = app.response_class(
        response=json.dumps(outdata),
        mimetype='application/json'
    )
    return response  

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'local':
        app.run(debug=True)
    else:
        app.run(host="ec2-18-130-215-119.eu-west-2.compute.amazonaws.com", port=80, debug=True)
