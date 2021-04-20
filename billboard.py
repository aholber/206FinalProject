from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json

#access billboard hot 100 url
url = "http://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20162017&seasonTo=20202021&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page=0&pageSize=100"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

ranking_list = []
name_list = []
points_list = []
final_list = []

#find all rankings, titles, artists, weeks
rankings = soup.find_all('div', class_='rt-td index-column rthfc-td-fixed rthfc-td-fixed-left')
names = soup.find_all('div', class_= 'rt-td rthfc-td-fixed rthfc-td-fixed-left rthfc-td-fixed-left-last')
points = soup.find_all('div', class_= 'rt-td primarySort')

for rank in rankings:
    ranking_list.append(rank.text.strip())
for name in names:
    name_list.append(name.text.strip())
for point in points:
    points_list.append(point.text.strip())

for i in range(len(ranking_list)):
    final_list.append((ranking_list[i], name_list[i], points_list[i]))
return tup_list


#strip and text when added to list of each 
# how do we wanna datdbase t his ishhh 