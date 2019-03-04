from flask import Flask, render_template
from flask_pymongo import PyMongo
from helpers import get_logo
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/rankit"
mongo = PyMongo(app)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    return 'Search Results Page'


@app.route('/institution/<int:UKPRN>')
def institution(UKPRN):
    inst = mongo.db.institutions.find_one({'UKPRN':UKPRN})
    #logo = get_logo(inst['PROVIDER_NAME'])
    logo = "/static/images/uoe_logo.png"
    print(logo)
    courses = mongo.db.courses.find({'UKPRN':UKPRN})
    return render_template('institution.html', inst=inst, courses=courses,
                           logo=logo)


@app.route('/course/<KISCOURSEID>')
def course(KISCOURSEID):
    course = mongo.db.courses.find_one({'KISCOURSEID':KISCOURSEID})
    return render_template('course.html', course=course)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/unis')
def unis():
    uni_list = mongo.db.institutions.find()
    return render_template('uni-list.html', uni_list = uni_list)

if __name__ == '__main__':
	app.run()
