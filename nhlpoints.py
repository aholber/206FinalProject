from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json

#def get_player_information():
url = "https://www.quanthockey.com/nhl/seasons/last-5-nhl-seasons-players-stats.html"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

namelist = []
pointlist = []
playerinfo = []

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