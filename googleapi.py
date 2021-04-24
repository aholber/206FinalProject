import requests
import json


def search():
    
    searchQuery = {
        'access_key': 'e2b362106cc9821f8ebfdc35e48c265b',
        'query': 'Patrick Kane'
    }

    searchData = requests.get('http://api.serpstack.com/search', searchQuery)

    searchResults = searchData.json()

    #print(searchResults)

    birthmonth = searchResults['knowledge_graph']['known_attributes'][0]['value'][0:3]
    
    info = searchResults['knowledge_graph']['known_attributes'][0]['value']
    info = info.split(',')
    birthcountry = info[-1]
    birthcountry = birthcountry.strip()
    if len(birthcountry) <= 2:
        birthcountry = 'United States'

    print(birthmonth)
    print(birthcountry)


search()

  