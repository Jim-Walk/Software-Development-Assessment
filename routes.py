from flask import Flask, render_template, request, json, redirect, url_for, abort, session
from flask_pymongo import PyMongo

from pymongo import MongoClient
client = MongoClient()
db = client.rankit

import random

from helpers import get_logo, get_wiki, rank_it
from models import SearchClass, Institutions, Courses

from copy import deepcopy

import math
from bson.json_util import dumps

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
    courses = Courses().GetTopPerInstitution(UKPRN)
    return render_template('institution.html', inst=inst, courses=courses,
                           logo=logo, wiki=wiki)

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
'''
@app.route('/rank', methods=['GET', 'POST'])
def rank():
    ###
    if request.method == 'GET':
        # First, retrieve form options
        department = request.args['department'].replace('+', ' ')
        salary = int(request.args['salary'])
        teach = int(request.args['teaching'])
        qol = request.args['qol']               # qol - Quality of Life
        employ = request.args['employ']         # employability

        # compile list of courses with no missing data
        courses = mongo.db.courses.find({"$text": {"$search": department}},
                                        limit=300)
        course_and_uni =[]
        c_list = []
        # get courses out of the pymongo cursor
        for course in courses:
            if not math.isnan(course['salary'][0]['MED']):
                if not math.isnan(course['nss'][0]['Q27']):
                    c_list += [course]

        for course in c_list:
            uni = mongo.db.institutions.find_one({'UKPRN':course['UKPRN']})
            if 'PROVIDER_NAME' in uni:
                course.update(uni)
                course_and_uni += [course]

        # rank list of courses
        c_final = rank_it(course_and_uni, salary, teach)
    return render_template('rank.html', courses=c_final)
    else:
    ###
    # First, retrieve form options

    course_name = request.form['course'].replace('+', ' ')

    salary = int(request.form['salary'])
    session['pref_salary'] = salary
    teach = int(request.form['teaching'])
    session['pref_studfeedback']

    # compile list of courses with no missing data
    courses = db.courses.find({"$text": {"$search": course_name}},
                                    limit=50)
    course_and_uni =[]
    c_list = []
    # get courses out of the pymongo cursor
    for course in courses:
        if not math.isnan(course['salary'][0]['MED']):
            if not math.isnan(course['nss'][0]['Q27']):
                c_list += [course]
    for course in c_list:
        uni = db.institutions.find_one({'UKPRN':course['UKPRN']})
        if 'PROVIDER_NAME' in uni:
            course.update(uni)
            course_and_uni += [course]
    # rank list of courses
    c_final = rank_it(course_and_uni, salary, teach)
    outdata = dumps(c_final)
    response = app.response_class(
        response=json.dumps(outdata),
        mimetype='application/json'
    )
    return response
'''

@app.route('/rank', methods=['GET', 'POST'])
def rank():
    pref_grad = request.form['grad_rates']
    session['pref_grad'] = pref_grad
    pref_empl = request.form['empl_chance']
    session['pref_empl'] = pref_empl
    pref_salary = request.form['salary']
    session['pref_salary'] = pref_salary
    pref_studfeed = request.form['teaching']
    session['pref_studfeed'] = pref_studfeed



    
if __name__ == '__main__':
    app.run(host="ec2-18-130-215-119.eu-west-2.compute.amazonaws.com", debug=True)