from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json

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