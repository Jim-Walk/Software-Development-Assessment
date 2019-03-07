from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from helpers import get_logo, get_wiki, rank_it
from copy import deepcopy
import math

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/rankit"
mongo = PyMongo(app)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    return render_template('search_result.html')


@app.route('/institution/<int:UKPRN>')
def institution(UKPRN):
    inst = mongo.db.institutions.find_one({'UKPRN':UKPRN})
    logo = get_logo(inst['PROVIDER_NAME'])
    #logo = "/static/images/uoe_logo.png" #in case you exceed the limit
    wiki = get_wiki(inst['PROVIDER_NAME'])
    courses = mongo.db.courses.find({'UKPRN':UKPRN})
    return render_template('institution.html', inst=inst, courses=courses,
                           logo=logo, wiki=wiki)

@app.route('/course/<PROVIDER_NAME>/<KISCOURSEID>')
def course(PROVIDER_NAME, KISCOURSEID):
    course = mongo.db.courses.find_one({'KISCOURSEID':KISCOURSEID})
    return render_template('course.html', course=course, university_name = PROVIDER_NAME)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/unis')
def unis():
    uni_list = mongo.db.institutions.find()
    return render_template('uni-list.html', uni_list = uni_list)

@app.route('/rank', methods=['GET'])
def rank():
    if request.method == 'GET':
        # First, retrieve form options
        department = request.args['department'].replace('+', ' ')
        salary = int(request.args['salary'])
        teach = int(request.args['teaching'])
        qol = request.args['qol']               # qol - Quality of Life
        employ = request.args['employ']         # employability

        # compile list of courses with no missing data
        courses = mongo.db.courses.find({"$text": {"$search": department}},
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

    return render_template('rank.html', courses=c_final)

if __name__ == '__main__':
	app.run()
