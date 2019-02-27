from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('base.html')


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
