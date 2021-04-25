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


def search():
    playerinfo = player_info()
    bigsearchResults = []
<<<<<<< HEAD
    goodnames = []
=======
    only_who_we_want = []
>>>>>>> e7b6f3815d1c2234d8841ab71157e42cd0f1e791

    for number in range(1,31):
        

        searchData = requests.get('https://statsapi.web.nhl.com/api/v1/teams/{}/roster'.format(number))

        searchResults = searchData.json()

        bigsearchResults.append(searchResults)
        

    bigsearchResults.remove({'messageNumber': 10, 'message': 'Object not found'})
    bigsearchResults.remove({'messageNumber': 10, 'message': 'Object not found'})

    idlist = []
    for i in bigsearchResults:
        for x in i['roster']:
            playerid = x['person']['id']
            idlist.append(playerid)

    

    for id in idlist:
        searchData = requests.get('https://statsapi.web.nhl.com/api/v1/people/{}'.format(id))
        searchResults = searchData.json()

        name = searchResults['people'][0]['fullName']
        birthmonth = searchResults['people'][0]['birthDate'][5:7]
        birthcountry = searchResults['people'][0]['birthCountry']

        #everybody = ((name, birthmonth, birthcountry))

<<<<<<< HEAD
        
        for player in playerinfo:
            if player[0] == name:
                goodnames.append((name, birthmonth, birthcountry))

    print(goodnames)

    return goodnames

=======
        for player in playerinfo:
            if player[0] == name:
                only_who_we_want.append((name, birthmonth, birthcountry))
    return only_who_we_want
        #print((name, birthmonth, birthcountry))
        #return (name, birthmonth, birthcountry)
>>>>>>> e7b6f3815d1c2234d8841ab71157e42cd0f1e791


def same_names():
    players = player_info()
    info = search()
    name_api_list = []
    the_best_list_ever = []
    
    for i in info:
        name_api_list.append(i[0])

    for player in players:
        if player[0] in name_api_list:
            the_best_list_ever.append(player)

    return the_best_list_ever


  