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

ranking_list = []
name_list = []
points_list = []
final_list = []

print(soup.find('div', class_='overflow-container'))

#find all rankings, names, and points for players
table = soup.find('div', class_='ReactTable -striped -highlight rthfc-knq8fb19 rthfc -sp')
table1 = table.find('div', class_='rt-tbody')
rows = table1.find_all('div', class_= 'rt-tr-group')

for row in rows:
    rankings = row.find_all('div', class_='rt-td index-column rthfc-td-fixed rthfc-td-fixed-left')
    names = row.find_all('div', class_= 'rt-td rthfc-td-fixed rthfc-td-fixed-left rthfc-td-fixed-left-last')
    points = row.find_all('div', class_= 'rt-td primarySort')

for rank in rankings:
    ranking_list.append(rank.text.strip())
for name in names:
    name_list.append(name.text.strip())
for point in points:
    points_list.append(point.text.strip())

for i in range(len(ranking_list)):
    final_list.append((ranking_list[i], name_list[i], points_list[i]))

print(final_list)


