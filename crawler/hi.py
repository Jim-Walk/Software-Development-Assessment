
#Import statements
import json
import requests
import pandas as pd
import xml.dom.minidom 
import xmltodict #This needs to be installed using pip install 

df= pd.read_csv('learning-providers-plus.csv')
url= 'https://data.unistats.ac.uk/api/v4/KIS/Institution/'

lista=[] # List storing all the entries  the UKPRN 
for index, row in df.iterrows():
   lista.append(row["UKPRN"])
   #asdasdasd

r = requests.get(url+str(lista[0]), auth=('37JNEZ7GVSN82RQDJ81R',''))
print(r.content)
    
dom = xml.dom.minidom.parseString(r.content)
pretty_xml_as_string = dom.toprettyxml()
print(pretty_xml_as_string)

print(json.dumps(xmltodict.parse(pretty_xml_as_string), indent=4))
    