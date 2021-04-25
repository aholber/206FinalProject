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
    only_who_we_want = []

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

        for player in playerinfo:
            if player[0] == name:
                only_who_we_want.append((name, birthmonth, birthcountry))
    return only_who_we_want
        #print((name, birthmonth, birthcountry))
        #return (name, birthmonth, birthcountry)


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

def other_same_names():
    players = player_info()
    info = search()
    points_website_list =[]
    another_great_list = []

    for player in players:
        points_website_list.append(player[0])
    
    for i in info:
        if i[0] in points_website_list:
            another_great_list.append(i)

    print(another_great_list)
    return another_great_list


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setup_players_table(cur, conn):
    data = same_names()
    cur.execute('CREATE TABLE IF NOT EXISTS Players (name TEXT PRIMARY KEY, points INTEGER)')
    for x in range(0,25):
        cur.execute('SELECT * FROM Players')
        rows = len(cur.fetchall())
        cur.execute('INSERT INTO Players ( name, points) VALUES (?, ?)', (data[rows][0], data[rows][1]))
    conn.commit()





def main():
    #search()
    #same_names()
    other_same_names()
    #cur, conn = setUpDatabase('players.db')
   # setup_players_table(cur, conn)
   # setup_players_table(cur, conn)
   # setup_players_table(cur, conn)
  #  setup_players_table(cur, conn)
   # setup_month_id(cur,conn)
    #etup_information_table(cur, conn)


if __name__ == "__main__":
    main()
