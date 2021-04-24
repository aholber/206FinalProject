from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json


def player_info():
    urls = []
    urls.append("https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Players&SS=5&af=0&nat=5&st=reg&sort=P&so=DESC&page=1&league=NHL&lang=en&rnd=434602094&dt=2&sd=undefined&ed=undefined")
    urls.append("https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Players&SS=5&af=0&nat=5&st=reg&sort=P&so=DESC&page=2&league=NHL&lang=en&rnd=704897555&dt=2&sd=undefined&ed=undefined")
    urls.append("https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Players&SS=5&af=0&nat=5&st=reg&sort=P&so=DESC&page=3&league=NHL&lang=en&rnd=102842642&dt=2&sd=undefined&ed=undefined")

    namelist = []
    pointlist = []
    playerinfo = []

    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        nametags = soup.find_all('a', class_="hl qh-nowrap")
        pointtags = soup.find_all('td', class_="sort-column")

        for nametag in nametags:
            nameinfo = nametag.text
            namelist.append(nameinfo)

        for pointtag in pointtags:
            pointinfo = pointtag.text
            pointlist.append(pointinfo)

        playerinfo = [(namelist[i], pointlist[i]) for i in range(0, len(namelist))]

    #print(playerinfo)
    return playerinfo




def search(player):
    
    searchQuery = {
        'access_key': 'e2b362106cc9821f8ebfdc35e48c265b',
        'query': player
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
        
    #print(birthmonth)
    #print(birthcountry)

    return player, birthmonth, birthcountry

for player in player_info():
    print(search(player[0]))

#earch()
