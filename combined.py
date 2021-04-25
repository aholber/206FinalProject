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
        'access_key': 'cffb9950e098f49f973ffb30e8f2274e',
        'query': player
    }

    searchData = requests.get('http://api.serpstack.com/search', searchQuery)

    searchResults = searchData.json()

    #print(searchResults)

    birthmonth = searchResults['knowledge_graph']['known_attributes'][0]['value'][0:3]
    if len(birthmonth) > 3:
        birthmonth = birthmonth[0:3]
    else:   
        birthmonth = birthmonth
    
    info = searchResults['knowledge_graph']['known_attributes'][0]['value']
    info = info.split(',')
    birthcountry = info[-1]
    birthcountry = birthcountry.strip()
    if len(birthcountry) <= 2:
        birthcountry = 'United States'
        
    #print(birthmonth)
    #print(birthcountry)

    return player, birthmonth, birthcountry

#
#    print(search(player[0]))

#search()
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setup_players_table(cur, conn):
    data = player_info()
    cur.execute('CREATE TABLE IF NOT EXISTS Players (name TEXT PRIMARY KEY, points INTEGER)')
    for x in range(0,25):
        cur.execute('SELECT * FROM Players')
        rows = len(cur.fetchall())
        cur.execute('INSERT INTO Players ( name, points) VALUES (?, ?)', (data[rows][0], data[rows][1]))
    conn.commit()


def setup_month_id(cur,conn):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cur.execute('CREATE TABLE IF NOT EXISTS Months_id (id INTEGER PRIMARY KEY, month TEXT)')  
    for i in range(len(months)):
        cur.execute('INSERT INTO Months_id (id, month) VALUES (?,?)', (i+1, months[i]))  
    conn.commit()


def setup_information_table(cur, conn):
    for player in player_info():
        data = search(player[0])
    cur.execute('CREATE TABLE IF NOT EXISTS Information (name TEXT PRIMARY KEY, month TEXT, country TEXT)')
    for x in range(0,25):
        cur.execute('SELECT * FROM Information')
        rows = len(cur.fetchall())
        cur.execute('INSERT INTO Players (name, month, country) VALUES (?, ?, ?)', (data[rows][0], data[rows][1], data[rows][2]))
    conn.commit()


def main():
    #player_info()
    cur, conn = setUpDatabase('players.db')
    setup_players_table(cur, conn)
    setup_players_table(cur, conn)
    setup_players_table(cur, conn)
    setup_players_table(cur, conn)
    setup_month_id(cur,conn)
    setup_information_table(cur, conn)


if __name__ == "__main__":
    main()