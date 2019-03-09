from database import *
from pymongo import MongoClient, TEXT
import pandas as pd
import csv, math
import pprint, random
import operator

client = MongoClient()
db = client.rankit


def int2(var):
	if math.isnan(var):
		return 0
	else:
		return int(var)


class Institutions(object):
	instcol = db.institutions

	def GetAll(self):
		cursor = self.instcol.find()
		result = []
		for doc in cursor:
			result.append(doc)
		result.sort(key=operator.itemgetter('UKPRN'))
		return result

	def Search(self, searchstr):
		cursor =  self.instcol.find({'$text' : { '$search': searchstr } })
		result = []
		for doc in cursor:
			result.append(doc)
		return result

	def GetByPRN(self, ukprn):
		result = self.instcol.find_one({'UKPRN' : int(ukprn)})
		return result

	def GetCourseIds(self, ukprn):
		inst = self.instcol.find_one({'UKPRN':ukprn})
		return inst["courses_ids"]


class Courses(object):

	coursecol = db.courses

	def Search(self, searchstr):
		cursor =  self.coursecol.find({'$text' : { '$search': searchstr } })
		result = []
		for doc in cursor:
			result.append(doc)
		return result

	def SearchByInstitution(self, searchstr, UKPRN):
		courses = self.Search(searchstr)
		result = []
		for course in courses:
			if course['UKPRN'] == UKPRN:
				result.append(course)
		return result

	def GetSingleByKIS(self, KIS):
		query = {'KISCOURSEID':KIS}
		return self.coursecol.find_one(query)

	def GetByInstitution(self, ukprn):
		query = {'UKPRN':ukprn}
		cursor = self.coursecol.find(query)
		result = []
		for doc in cursor:
			result.append(doc)
		return result

	def GetBySubject(self, cah_code):
		query = {'subject_cah':cah_code}

		cursor = self.coursecol.find(query).sort('UKPRN', 1)
		result = []
		for doc in cursor:
			result.append(doc)	
		return result

	def GetRelatedBySubject(self, KIS):
		course = self.GetSingleByKIS(KIS)
		cah = course['subject_cah']
		prn = course['UKPRN']
		query = {'subject_cah':cah, 'UKPRN': prn}
		cursor = self.coursecol.find(query)
		courses = []
		for doc in cursor:
			courses.append(doc)
		random.shuffle(courses)
		return courses[0:10]

	def GetTopPerInstitution(self, UKPRN):
		courses = self.GetByInstitution(UKPRN)

		courses.sort(key=lambda k: k['nss'][0]['Q27'], reverse=True)
		return courses[0:10]



class SearchClass(object):
	"""docstring for Search"""
	def __init__(self):
		self.courses = Courses()
		self.institutions = Institutions()

	def GlobalSearch(self, string):
		result = self.institutions.Search(string)
		for inst in result:
			inst['courses_list'] = Courses().SearchByInstitution(string, inst['UKPRN'])
		return result



if __name__ == '__main__':
	#pprint.pprint(Courses().GetTopPerInstitution(10007166, 30, 40, 50, 40))
	pprint.pprint(Institutions().GetByPRN(10007150))

		
