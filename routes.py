from flask import Flask, render_template, request, json
from flask_pymongo import PyMongo
from helpers import get_logo, get_wiki, rank_it
from copy import deepcopy
import math
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/rankit"
mongo = PyMongo(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    list_uni = mongo.db.institutions.find()
    #indata = request.form #incoming data
    outdata = dumps(list_uni)
    response = app.response_class(
        response=json.dumps(outdata),
        mimetype='application/json'
    )
    return response

@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        search_str = request.args['searchInput'].replace('+', ' ')
        courses = mongo.db.courses.find({"$text": {"$search": search_str}},
                                        limit=10)
        unis = mongo.db.institutions.find({"$text": {"$search": search_str}},
                                        limit=10)
        uni_list = []
        course_list = []

        # extract values from mongo cursor before we can use them
        for uni in unis:
            uni_list += [uni]

        for course in courses:
            course_list += [course]
        for course in course_list:
            uni = mongo.db.institutions.find_one({'UKPRN': course['UKPRN']})
            course.update(uni)

    return render_template('search_result.html', courses=course_list,
                           unis=uni_list)


@app.route('/institution/<int:UKPRN>')
def institution(UKPRN):
    inst = mongo.db.institutions.find_one({'UKPRN':UKPRN})
    #logo = get_logo(inst['PROVIDER_NAME'])
    logo = "/static/images/uoe_logo.png" #in case you exceed the limit
    wiki = get_wiki(inst['PROVIDER_NAME'])
    courses = mongo.db.courses.find({'UKPRN':UKPRN}, limit=7)
    return render_template('institution.html', inst=inst, courses=courses,
                           logo=logo, wiki=wiki)

@app.route('/course/<PROVIDER_NAME>/<KISCOURSEID>')
def course(PROVIDER_NAME, KISCOURSEID):
    date = 'September, 2019'
    deadline = '10 May 2019'
    modes = 'Full time'
    duration = '4 years'
    course = mongo.db.courses.find_one({'KISCOURSEID':KISCOURSEID})
    return render_template('course.html', 
                            course=course, 
                            university_name = PROVIDER_NAME, 
                            date=date,
                            deadline = deadline,
                            modes = modes,
                            duration = duration
                           )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/unis')
def unis():
    uni_list = mongo.db.institutions.find()
    return render_template('uni-list.html', uni_list = uni_list)

@app.route('/rank', methods=['GET', 'POST'])
def rank():
    '''
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
    '''    
    # First, retrieve form options
    course_name = request.form['course'].replace('+', ' ')
    salary = int(request.form['salary'])
    teach = int(request.form['teaching'])

    # compile list of courses with no missing data
    courses = mongo.db.courses.find({"$text": {"$search": course_name}},
                                    limit=50)
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
    outdata = dumps(c_final)
    response = app.response_class(
        response=json.dumps(outdata),
        mimetype='application/json'
    )
    return response








if __name__ == '__main__':
	app.run(host="ec2-18-130-215-119.eu-west-2.compute.amazonaws.com")
