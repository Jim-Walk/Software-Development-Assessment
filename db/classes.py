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
		self.ImportNSS()
		self.ImportSalary()

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
		self.institutions.create_index([('$**', 'text')])

	def DropDB(self):
		db.command('dropDatabase')
		print('Database Dropped')

	def ImportNSS(self):
		df = pd.read_csv('./data/NSS.csv')
		print('Importing NSS')
		for index,row in df.iterrows():
			if index%1000 == 0:
					print(str(index)+' out of '+str(df.size) + ' NSS entries')
			entry = row.to_dict()
			kiscourseid = entry["KISCOURSEID"]
			entry.pop('PUBUKPRN')
			entry.pop('UKPRN')
			entry.pop('KISCOURSEID')
			entry.pop('KISMODE')
			self.courses.update({'KISCOURSEID':kiscourseid}, { '$push': { 'nss': entry} }, upsert=True )
		self.courses.create_index([('$**', 'text')])
		df = pd.read_csv('./data/NHSNSS.csv')
		print('Importing NHSNSS')
		for index,row in df.iterrows():
			if index%1000 == 0:
					print(str(index)+' out of '+str(df.size) + ' NHS NSS entries')
			entry = row.to_dict()
			kiscourseid = entry["KISCOURSEID"]
			entry.pop('PUBUKPRN')
			entry.pop('UKPRN')
			entry.pop('KISCOURSEID')
			entry.pop('KISMODE')
			self.courses.update({'KISCOURSEID':kiscourseid}, { '$push': { 'nss': entry} }, upsert=True )
		self.courses.create_index([('$**', 'text')])


	def ImportSalary(self):
		df = pd.read_csv('./data/SALARY.csv')
		print('Importing Salary')
		for index,row in df.iterrows():
			if index%1000 == 0:
					print(str(index)+' out of '+str(df.size) + ' salaries')
			entry = row.to_dict()
			kiscourseid = entry["KISCOURSEID"]
			entry.pop('PUBUKPRN')
			entry.pop('UKPRN')
			entry.pop('KISCOURSEID')
			entry.pop('KISMODE')
			self.courses.update({'KISCOURSEID':kiscourseid}, { '$push': { 'salary': entry} }, upsert=True )
		self.courses.create_index([('$**', 'text')])

	def ImportGraduationRates(self):
		df = pd.read_csv('./data/DEGREECLASS.csv')
		print("Adding Graduation Rate")
		for index,row in df.iterrows():
			if index%1000 == 0:
					print(str(index)+' out of '+str(df.size) + ' graduation rates')
			entry = row.to_dict()
			kiscourseid = entry["KISCOURSEID"]
			self.courses.update({'KISCOURSEID':kiscourseid}, { '$push': { 'graduation_rate_percent': entry["UPASS"]} }, upsert=True )

	def ImportEmploymentRates(self):
		df = pd.read_csv('./data/EMPLOYMENT.csv')
		print("Adding Employment Rates 6M post-graduation")
		for index,row in df.iterrows():
			if index%1000 == 0:
					print(str(index)+' out of '+str(df.size) + ' employment rates')
			entry = row.to_dict()
			kiscourseid = entry["KISCOURSEID"]
			self.courses.update({'KISCOURSEID':kiscourseid}, { '$push': { 'employment_rate_percent': entry["WORKSTUDY"]} }, upsert=True )

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

