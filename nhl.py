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

#print(soup.find('div', class_='overflow-container'))

#find all rankings, names, and points for players
first_table = soup.find('div', class_='overflow-container')
#sec_table = first_table.find('div', class_='dataTables_wrapper no-footer')
#another_table = sec_table.find_all('div', class_= 'DTFC_ScrrollWrapper')
table = first_table.find('div', class_='dataTables_scroll')

body1 = table.find('div', class_='dataTables_scrollBody')
the_body = body1.find('div', class_='ps_tbl no wrap dt3 dataTable no-footer')

rows_odd = the_body.find_all('tr', class_='odd')
for row in rows_odd:
    rankings = row.find_all('td', class_='alignleft')
    names = row.find_all('a', class_= 'hl qh-nowrap')
    points = row.find_all('td', class_= 'sort-column')

for rank in rankings:
    ranking_list.append(rank.text.strip())
for name in names:
    name_list.append(name.text.strip())
for point in points:
    points_list.append(point.text.strip())

for i in range(len(ranking_list)):
    final_list.append((ranking_list[i], name_list[i], points_list[i]))

#print(final_list)


