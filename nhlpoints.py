from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json

def get_player_info():
    urls = []
    urls.append("https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Players&SS=5&af=0&nat=5&st=reg&sort=P&so=DESC&page=1&league=NHL&lang=en&rnd=434602094&dt=2&sd=undefined&ed=undefined")
    urls.append("https://www.quanthockey.com/scripts/AjaxPaginate.php?cat=Season&pos=Players&SS=5&af=0&nat=5&st=reg&sort=P&so=DESC&page=2&league=NHL&lang=en&rnd=704897555&dt=2&sd=undefined&ed=undefined")

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
    print(playerinfo)
    return playerinfo


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setup_players_table(cur, conn):
    data = get_player_info()
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




def main():
    get_player_info()
    cur, conn = setUpDatabase('players.db')
    setup_players_table(cur, conn)
    setup_players_table(cur, conn)
    setup_players_table(cur, conn)
    #setup_players_table(cur, conn)
    setup_month_id(cur,conn)


if __name__ == "__main__":
    main()