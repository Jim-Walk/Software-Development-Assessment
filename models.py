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

	def GetByPRNList(self,list):
		result = []
		for prn in list:
			result.append(self.GetByPRN(prn))
		return result

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
		if len(result) > 0:
			for inst in result:
				inst['courses_list'] = Courses().SearchByInstitution(string, inst['UKPRN'])
			return result
		else:
			courses = Courses().Search(string)
			ukprns = []
			for course in courses:
				if course['UKPRN'] not in ukprns:
					ukprns.append(course)
			for prn in ukprns:
				result.append(Institutions().GetByPRN(prn))
			for inst in result:
				inst['courses_list'] = Courses().SearchByInstitution(string, inst['UKPRN'])
			return result
'''
'''
class RankClass(object):
	def __init__(self, subject_code, pref_grad, pref_empl, pref_salary, pref_studfeed):
		self.courses = Courses()
		self.institutions = Institutions()
		self.grad = pref_grad
		self.empl = pref_empl
		self.salary = pref_salary
		self.studfeed = pref_studfeed
		self.subject = subject_code



	def GetResult(self):
		courses_bysubject = self.courses.GetBySubject(self.subject)
		for idx,course in enumerate(courses_bysubject):
			grad_pts = course['graduation_rate_percent'] * self.grad
			empl_pts = course['employment_rate_percent'] * self.empl 
			salary_pts = course['median_salary'] *  self.salary
			studfeed_pts = course['studentsatisfaction_rate_percent'] * self.studfeed
			course['tot_points'] = 	grad_pts + empl_pts + salary_pts + studfeed_pts
			if course['tot_points'] <= 0.0:
				courses_bysubject.pop(idx)
		courses_bysubject.sort(key=operator.itemgetter('tot_points'))
		institution_scores = {}
		for idx,course in enumerate(courses_bysubject):
			if course['UKPRN'] not in institution_scores:
				institution_scores[course['UKPRN']] = len(courses_bysubject) - idx 
			else:
				institution_scores[course['UKPRN']] += len(courses_bysubject) - idx
		ranked_prns = []
		for key, value in sorted(institution_scores.items(), key=operator.itemgetter(1)):
			ranked_prns.append(Institutions.GetByPRN(key))
		return ranked_prns
		
if __name__ == '__main__':
	r = RankClass('CAH01', 50, 50, 50, 50)
	r.GetResult()