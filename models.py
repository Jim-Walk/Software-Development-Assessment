from database import *
from pymongo import MongoClient, TEXT
import pandas as pd
import csv, math, pprint, random, operator

client = MongoClient()
db = client.rankit


class Institutions(object):
	instcol = db.institutions

	def GetByPRNList(self,list): #Get a list of institutions from a list of PRNs
		result = []
		for prn in list:
			result.append(self.GetByPRN(prn))
		return result

	def GetAll(self):# Get All institutions as a list.
		cursor = self.instcol.find()
		result = []
		for doc in cursor:
			result.append(doc)
		result.sort(key=operator.itemgetter('UKPRN'))
		return result

	def Search(self, searchstr): #Search institution by text query
		cursor =  self.instcol.find({'$text' : { '$search': searchstr } })
		result = []
		for doc in cursor:
			result.append(doc)
		return result

	def GetByPRN(self, ukprn): #get a single institution, as dict
		result = self.instcol.find_one({'UKPRN' : int(ukprn)})
		return result

	def GetCourseIds(self, ukprn): #Get all KISCOURSEIDs for courses available at this institution
		inst = self.instcol.find_one({'UKPRN':ukprn})
		return inst["courses_ids"]


class Courses(object):

	coursecol = db.courses

	def GetAll(self):
		cursor = self.coursecol.find()
		result = []
		for doc in cursor:
			result.append(doc)
		return result

	def Search(self, searchstr): #Search courses by query string, returns a list of courses(Dicts)
		cursor =  self.coursecol.find({'$text' : { '$search': searchstr } })
		result = []
		for doc in cursor:
			result.append(doc)
		return result

	def SearchByInstitution(self, searchstr, UKPRN): #Search courses with a query string, constrained to an institution
		courses = self.Search(searchstr)
		result = []
		for course in courses:
			if course['UKPRN'] == UKPRN:
				result.append(course)
		return result

	def GetSingleByKIS(self, KIS): #Get a single course by it's KISCOUSEID, as a dict
		query = {'KISCOURSEID':KIS}
		return self.coursecol.find_one(query)

	def GetByInstitution(self, ukprn): #Get all courses available at an institution, list of courses(dicts)
		query = {'UKPRN':ukprn}
		cursor = self.coursecol.find(query)
		result = []
		for doc in cursor:
			result.append(doc)
		return result

	def GetBySubject(self, cah_code): #Get all courses from a given subject, by CAH(subject) code. See data/CAH.csv for cah code descriptions
		query = {'subject_cah':cah_code}

		cursor = self.coursecol.find(query).sort('UKPRN', 1)
		result = []
		for doc in cursor:
			result.append(doc)	
		return result

	def GetRelatedBySubject(self, KIS): #get a list of courses, related to a given course by KISCOURSEID, in the same institution as the root (passed to this function) course
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

	def GetTopPerInstitution(self, UKPRN): #Gets the top ranked courses by student feedback
		courses = self.GetByInstitution(UKPRN)

		courses.sort(key=lambda k: k['nss'][0]['Q27'], reverse=True)
		return courses[0:10]



class SearchClass(object):
	"""docstring for Search"""
	def __init__(self):
		self.courses = Courses()
		self.institutions = Institutions()

	def GlobalSearch(self, string): #Search across institutions and courses, returns a list of institutions (dict), each institution dict containing a list of courses (dicts)
		result = self.institutions.Search(string)
		if len(result) > 0: # the user has probably made a composite search (course title + institution name or location) ie: "edinburgh computer science"
			for inst in result:
				inst['courses_list'] = Courses().SearchByInstitution(string, inst['UKPRN'])
			return result
		else: #the user is probably searching for a course only, not an institution ie: "computer science"
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
		salaries = []
		#compute max a min salaries from the courses, to normalize each course's salary
		for course in courses_bysubject:
			salaries.append(course['median_salary'])
		return(salaries)
		salary_min = min(salaries)
		salary_range = max(salaries) - salary_min
		#iterate over courses
		for idx,course in enumerate(courses_bysubject):
			if math.isnan(course['graduation_rate_percent']) or math.isnan(course['employment_rate_percent']) or math.isnan(course['median_salary']) or math.isnan(course['studentsatisfaction_rate_percent']):
					#if any of the criteria is not a number, skip the course
					continue
			grad_pts = int(course['graduation_rate_percent'] * self.grad)
			empl_pts = int(course['employment_rate_percent'] * self.empl)
			normal_salary = int(((course['median_salary']) - salary_min) / salary_range)
			salary_pts = int(normal_salary *  self.salary)
			studfeed_pts = int(course['studentsatisfaction_rate_percent'] * self.studfeed)
			if (grad_pts <= 0.0) or (empl_pts <= 0.0) or (salary_pts <= 0.0) or (studfeed_pts <= 0.0):
				#remove the course if any of the points yields zero, arbitrary but to be improved
				courses_bysubject.pop(idx)
			#add the points to the course dict
			course['tot_points'] = 	grad_pts + empl_pts + salary_pts + studfeed_pts
		courses_bysubject.sort(key=operator.itemgetter('tot_points'))
		institution_scores = {} #group individual course scores by institutions (by UKPRNs)
		for idx,course in enumerate(courses_bysubject):
			if course['UKPRN'] not in institution_scores:
				institution_scores[course['UKPRN']] = len(courses_bysubject) - idx 
			else:
				institution_scores[course['UKPRN']] += len(courses_bysubject) - idx
		ranked_prns = []
		for key, value in sorted(institution_scores.items(), key=operator.itemgetter(1), reverse=True):
			#iterate over the institution scores dict, by value (=the total points obtained)
			ranked_prns.append(Institutions.GetByPRN(key)) #append the final "leaderboard" to the list, index of the list determining the index
		return ranked_prns
