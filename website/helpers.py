import requests
import config
import wikipediaapi
from titlecase import titlecase

# Takes as input a univerity's title field, returns 
# the logo of that university through a google API query.
# NOTE: This API is only valid for 100 requests per day
def get_logo(uni_title):
    url ='https://www.googleapis.com/customsearch/v1?searchType=image&cx=011314089285855499136%3Ata88ozaawbs&num=1&fields=items(link)'+config.API_KEY
    # construct query string using a list comprhension
    # convert spaces to %20
    query = '&q=' + uni_title.replace(' ', '%20') + '%20logo'
    r = requests.get(url+query)
    return r.json()['items'][0]['link']


def get_wiki(uni_title):
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(titlecase(uni_title))
    if page.exists():
        print('we get here')
        return {'url': page.fullurl, 'summary': page.summary[0:1000]}
    else:
        return {'summary': "Unable to find wikipedia page "}

# Takes a list of course and uni dicts, sorts them 
# according to weight factors
def rank_it(c_list, salary, teach):
    if teach > salary:
        return sorted(c_list, key=lambda k: k['nss'][0]['Q27'], reverse=True)
    else:
        return sorted(c_list, key=lambda k: k['salary'][0]['MED'], reverse=True)

