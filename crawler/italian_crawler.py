import urllib3

http = urllib3.PoolManager()

#Based on API query examples shown here http://dati.ustat.miur.it/dataset/laureati-anno-solare-2017/resource/88acd482-9d75-44d1-ab16-aa04524f5d94?view_id=80febbd5-17a7-4a94-95a3-9a471cf43783

#Sample query for results that include Jones
r = http.request('GET', 'http://dati.ustat.miur.it/api/3/action/datastore_search?resource_id=88acd482-9d75-44d1-ab16-aa04524f5d94&limit=5&q=title:jones')

#Sample query for the first 5 results
r2= http.request('GET', 'http://dati.ustat.miur.it/api/3/action/datastore_search?resource_id=88acd482-9d75-44d1-ab16-aa04524f5d94&limit=5')

print(r2.data)

#Need to convert this into JSON file