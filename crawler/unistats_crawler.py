#This is a working script for generating a JSON file from the Unistats website.
#The learning-providers-plus.csv file is used in order to pick a UKPRN ID number which will be used in the HTTP
#request made to the Unistats website.

import requests
import pandas as pd
import lxml.etree as etree
import xmltodict
import simplejson as json

df= pd.read_csv('learning-providers-plus.csv')
url = 'https://data.unistats.ac.uk/api/v4/KIS/Institution/'

lista=[] # List storing all the entries the UKPRN
for index, row in df.iterrows():
   lista.append(row["UKPRN"])

r = requests.get(url+str(lista[0]), auth=('37JNEZ7GVSN82RQDJ81R','')) #We just use the first entry, which is UKRPN = 10008640

with open('output.xml', 'wb') as handle:
   for block in r.iter_content(1024):
      handle.write(block)

x = etree.parse('output.xml')
parsed=etree.tostring(x, pretty_print=True)

print(json.dumps(xmltodict.parse(parsed), indent=4))

