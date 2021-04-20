import requests
import json


def search():
    
    searchQuery = {
        'access_key': 'e2b362106cc9821f8ebfdc35e48c265b',
        'query': 'Connor McDavid'
    }

    searchData = requests.get('http://api.serpstack.com/search', searchQuery)

    searchResults = searchData.json()

    birthmonth = searchResults['knowledge_graph']['known_attributes'][0]['value'][0:3]
    print(birthmonth)


search()