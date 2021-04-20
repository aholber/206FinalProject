from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json

#access billboard hot 100 url
url = "https://www.billboard.com/charts/hot-100"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

ranking_list = []
artist_list = []
song_list = []
weeks_list = []

#find all rankings, titles, artists, weeks
rankings = soup.find_all('span', class_='chart-element__rank__number')
titles = soup.find_all('span', class_= 'chart-element__information__song text--truncate color--primary')
artists = soup.find_all('span', class_= 'chart-element__information__song text--truncate color--secondary')
weeks = soup.find_all('div', class_= 'chart-element__meta text--center color--secondary text--week')

#strip and text when added to list of each 
# how do we wanna datdbase t his ishhh 