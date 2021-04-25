from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json




<<<<<<< HEAD
def search():
    
=======
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

    print(playerinfo)
    return playerinfo


def search():
    playerinfo = player_info()
>>>>>>> 5be7ca714ac11d2abf0ba539a87570539d826d45
    bigsearchResults = []

    for number in range(1,31):
        

        searchData = requests.get('https://statsapi.web.nhl.com/api/v1/teams/{}/roster'.format(number))

        searchResults = searchData.json()

        bigsearchResults.append(searchResults)
        

    bigsearchResults.remove({'messageNumber': 10, 'message': 'Object not found'})
    bigsearchResults.remove({'messageNumber': 10, 'message': 'Object not found'})

    idlist = []
    totallist = []

    for i in bigsearchResults:
        for x in i['roster']:
            playerid = x['person']['id']
            idlist.append(playerid)

    for id in idlist[:60]:
        searchData = requests.get('https://statsapi.web.nhl.com/api/v1/people/{}'.format(id))
        searchResults = searchData.json()

        name = searchResults['people'][0]['fullName']
        birthmonth = searchResults['people'][0]['birthDate'][5:7]
        birthcountry = searchResults['people'][0]['birthCountry']

<<<<<<< HEAD
        full = name, birthmonth, birthcountry 

        totallist.append(full)
    #print(totallist)
    return totallist


def player_info():
    urls = []
    urls.append("https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Players&SS=5&af=0&nat=5&st=reg&sort=P&so=DESC&page=1&league=NHL&lang=en&rnd=434602094&dt=2&sd=undefined&ed=undefined")
    urls.append("https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Players&SS=5&af=0&nat=5&st=reg&sort=P&so=DESC&page=2&league=NHL&lang=en&rnd=704897555&dt=2&sd=undefined&ed=undefined")
    urls.append("https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Players&SS=5&af=0&nat=5&st=reg&sort=P&so=DESC&page=3&league=NHL&lang=en&rnd=102842642&dt=2&sd=undefined&ed=undefined")

    namelist = []
    pointlist = []
    playerinfo = []

    search = search()

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


    for player in search:
        #if player[0] == playerinfo[0]:
        print(player)

    return playerinfo
=======
        #everybody = ((name, birthmonth, birthcountry))

        only_who_we_want = []
        for player in playerinfo:
            if player[0] == name:
                only_who_we_want.append((name, birthmonth, birthcountry))
            for i in only_who_we_want:
                if i == '[]':
                    i = ''
        print(only_who_we_want)
        #print((name, birthmonth, birthcountry))
        #return (name, birthmonth, birthcountry)


player_info()
search()    
>>>>>>> 5be7ca714ac11d2abf0ba539a87570539d826d45

search = search()
player_info()