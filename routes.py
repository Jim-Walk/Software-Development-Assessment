from flask import Flask
app = Flask(__name__)

@app.route('/')
def main():
    return 'Index Page'


@app.route('/search', methods=['GET'])
def search():
    return 'Search Results Page'


@app.route('/institution/<int:UKPRN>')
def institution():
    return 'Institution Page'


@app.route('/course/<KISCOURSEID>')
def course():
    return 'Course Page'



if __name__ == '__main__':
	app.run()