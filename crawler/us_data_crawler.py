import requests

#Taken from here https://github.com/RTICWDT/open-data-maker/blob/master/API.md
#In this query URL:
#https://api.data.gov/ed/collegescorecard/v1/ is the URL Path.
#v1 is the API Version String, followed by /, which separates it from the Endpoint.
#schools is the Endpoint. Note the plural.
#.json is the Format. Note the dot between the Endpoint and Format. Also note that, since JSON is the default output format, we didn't have to specify it.
#In keeping with standard URI Query String syntax, the ? and & characters are used to begin and separate the list of query parameters.
#school.degrees_awarded.predominant=2,3 is a Field Parameter. In this case, it's searching for records which have a school.degrees_awarded.predominant value of either 2 or 3.
#_fields=id,school.name,2013.student.size is an Option Parameter, as denoted by the initial underscore character. _fields is used to limit the output fields to those in the given list. We strongly recommend using the _fields parameter to reduce the amount of data returned by the API, thus increasing performance.

r2 = requests.get('https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&_fields=id,school.name,2013.student.size&api_key=yphysq0h5Otab7UxqJlz9cHWzL32eSCVznZ8YwbR')
print(r2.content)

#Having issues with converting this to a JSON object


