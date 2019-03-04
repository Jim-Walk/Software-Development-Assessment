import requests
import config

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

