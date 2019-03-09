from database import *
from pymongo import MongoClient, TEXT
import pandas as pd
import csv
import pprint, random

client = MongoClient()
db = client.rankit




class Institutions(object):
	instcol = db.institutions

	def GetAll(self):
		return self.instcol.find()

	def Search(self, searchstr):
		cursor =  self.instcol.find({'$text' : { '$search': searchstr } }).limit(10)
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
		cursor =  self.coursecol.find({'$text' : { '$search': searchstr } }).limit(10)
		result = []
		for doc in cursor:
			result.append(doc)
		return result

	def GetSingleByKIS(self, KIS):
		query = {'KISCOURSEID':KIS}
		return self.coursecol.find_one(query)

	def GetByInstitution(self, ukprn):
		query = {'UKPRN':ukprn}
		cursor = self.coursecol.find(query).limit(10)
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

	def GetTopPerInstitution(self, UKPRN, pref_grad, pref_empl, pref_salary, pref_studfeedback):
		return True



class SearchClass(object):
	"""docstring for Search"""
	def __init__(self):
		self.courses = Courses()
		self.institutions = Institutions()

	def GlobalSearch(self, string):
		result = {}
		courses_res = self.courses.Search(string)
		instit_res = self.institutions.Search(string)
		result["courses"] = courses_res
		result["institutions"] = instit_res
		return result



if __name__ == '__main__':
	pprint.pprint(Courses().GetByInstitution(10007166))
	#pprint.pprint(Institutions().GetByPRN(10007166))

		
