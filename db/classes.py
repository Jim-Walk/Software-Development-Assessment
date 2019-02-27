from pymongo import MongoClient, TEXT
import pandas as pd
client = MongoClient()
db = client.rankit


class Database(object):
	"""docstring for Database"""
	db = MongoClient().rankit
	institutions = db.institutions
	courses = db.courses

	def Bootstrap(self):
		self.ImportInstitutions()
		self.ImportCourses()
		self.ImportLocations()

	def ImportInstitutions(self):
		print('Importing Institutions...')
		self.institutions.create_index([('$**', 'text')])
		df = pd.read_csv('./data/learning-providers.csv')
		for index,row in df.iterrows():
			entry = row.to_dict()
			entry['courses_ids'] = []
			entry['locations'] = []
			self.institutions.update({'UKPRN':entry['UKPRN']}, entry, upsert=True)
	def ImportCourses(self):
		print('Importing Courses...')
		df = pd.read_csv('./data/KISCOURSE.csv', low_memory=False)
		for index,row in df.iterrows():
			if index%1000 == 0:
					print(str(index)+' out of '+str(df.size) + ' courses')
			entry = row.to_dict()
			ukprn = entry['UKPRN']
			kiscourseid = entry['KISCOURSEID']
			self.courses.update({'KISCOURSEID':kiscourseid}, entry, upsert=True)
			self.institutions.update( {'UKPRN':ukprn}, { '$push': { 'courses_ids': kiscourseid } }, upsert=True )
		self.courses.create_index([('$**', 'text')])

	def ImportLocations(self):
		df = pd.read_csv('./data/LOCATION.csv')
		print('Importing Locations')
		for index,row in df.iterrows():
			if index%1000 == 0:
					print(str(index)+' out of '+str(df.size) + ' locations')
			entry = row.to_dict()
			ukprn = entry['UKPRN']
			entry.pop('UKPRN')
			self.institutions.update( {'UKPRN':ukprn}, { '$push': { 'locations': entry } }, upsert=True )
		self.courses.create_index([('$**', 'text')])

	def DropDB(self):
		db.command('dropDatabase')
		print('Database Dropped')

class Institution(object):
	instcol = db.institutions

	def Search(self, searchstr):
		print('Searching ' + searchstr)
		return self.instcol.find({'$text' : { '$search': searchstr } })

	def GetByPRN(self, ukprn):
		return self.instcol.find({'UKPRN' : ukprn})

	def GetCourseIds(self, ukprn):
		inst = self.instcol.find()
		return inst

class Course(object):

	coursecol = db.courses

	def Search(self, string):
		return self.coursecol.find({'$text' : {'$search': string} })

	def GetByKIS(self, KIS):
		query = {'KISCOURSEID':KIS}
		return self.coursecol.find_one(query)

	def GetByInstitution(self, ukprn):
		query = {'UKPRN':ukprn}
		return self.coursecol.find_one(query)
