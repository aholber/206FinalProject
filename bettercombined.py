from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json


def player_info():
    """No inputs. Returns a list of tuples in which the contents are (player, point total). Does this for 150 players."""
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
    """No inputs. Returns a list of tuples in which the contents are (player, birth month, country). Does this for every single player in the league."""
    playerinfo = player_info()
    bigsearchResults = []
    goodnames = []

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

        for player in playerinfo:
            if player[0] == name:
                goodnames.append((name, birthmonth, birthcountry))

    return goodnames


def same_names():
    """No inputs. Returns a list of tuples in which the contents are (player, point total). Does this only for players that coincide with both lists."""
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
    """No inputs. Returns a list of tuples in which the contents are (player, birth month, country). Does this only for players that coincide with both lists."""
    players = player_info()
    info = search()
    points_website_list =[]
    another_great_list = []

    for player in players:
        points_website_list.append(player[0])
    
    for i in info:
        if i[0] in points_website_list:
            another_great_list.append(i)

    return another_great_list


def setUpDatabase(db_name):
    """Takes the name of a database, a string, as an input. Returns the cursor and connection to the database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setup_players_table(cur, conn):
    """Takes the database cursor and connection as inputs. Returns nothing. Inserts into the table all of the player names and their corresponding point totals over the last 5 years."""
    data = same_names()
    cur.execute('CREATE TABLE IF NOT EXISTS Players (name TEXT PRIMARY KEY, points INTEGER)')
    for x in range(0,25):
        cur.execute('SELECT COUNT(name) FROM Players')
        rows = cur.fetchone()[0]
        cur.execute('INSERT INTO Players (name, points) VALUES (?, ?)', (data[rows][0], data[rows][1]))
    conn.commit()


def set_up_country_table(cur, conn):
    """Takes the database cursor and connection as inputs. Returns nothing. Inserts into the table all of the player countries and a corresponding id number."""
    counts = ['USA', 'CAN', 'SWE', 'RUS', 'CZE', 'SVK', 'CHE', 'FIN', 'DEU', 'SVN', 'NOR']
    cur.execute('CREATE TABLE IF NOT EXISTS Countries (id INTEGER PRIMARY KEY, country TEXT)')
    for i in range(len(counts)):
        cur.execute('INSERT INTO Countries (id, country) VALUES (?,?)', (i+1, counts[i]))
    conn.commit()


def setup_month_id(cur,conn):
    """Takes the database cursor and connection as inputs. Returns nothing. Inserts into the table all of the birth months and a corresponding id number."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cur.execute('CREATE TABLE IF NOT EXISTS Months_id (id INTEGER PRIMARY KEY, month TEXT)')  
    for i in range(len(months)):
        cur.execute('INSERT INTO Months_id (id, month) VALUES (?,?)', (i+1, months[i]))  
    conn.commit()


def birth_info_table(cur, conn):
    """Takes the database cursor and connection as inputs. Returns nothing. Inserts into the table all of the player names, and both their corresponding birth months and birth countries."""
    info = other_same_names()
    #cur.execute('SELECT id FROM Countries WHERE country = ? ', info[rows][2])
    #c = cur.fetchone()[0]
    cur.execute('CREATE TABLE IF NOT EXISTS Birthdays (name TEXT PRIMARY KEY, birth_month INTEGER, birth_place TEXT)')
    count = 0
    while count < 25: 
        cur.execute('SELECT COUNT(name) FROM Birthdays')
        rows = cur.fetchone()[0]
        cur.execute('INSERT OR IGNORE INTO Birthdays (name, birth_month, birth_place) VALUES (?, ?, ?)', (info[rows][0], info[rows][1], info[rows][2]))
        if cur.rowcount > 0:
            count += 1
    conn.commit()


##calculations begin here!!!

def return_top_ten_players():
    """Takes nothing as input. Returns the top 10 players and their point totals over the past 5 years in the NHL."""
    top_ten_list = []
    playerinfo = player_info()
    for player in playerinfo[:10]:
        top_ten_list.append(player[0]+ " has " + player[1] + " points over the last 5 seasons in the NHL.")

    print(top_ten_list)
    return top_ten_list

def return_average_points():
    """Takes nothing as input. Returns the average number of points of the top 10 players over the past 5 years in the NHL in a statement."""
    top_ten_list = []
    top_ten_point_totals = []
    playerinfo = player_info()
    for player in playerinfo[:10]:
        top_ten_list.append(player)
    for i in top_ten_list:
        top_ten_point_totals.append(int(i[1]))
    
    count = 0
    division = len(top_ten_point_totals)
    for num in top_ten_point_totals:
        count += num
    
    average = int(count / division)

    statement = "The average number of points over the past 5 seasons by the top 10 players is {}.".format(average)
    print(statement)
    return statement

def write_data_to_file(filename):
    """Takes in a filename (string) as an input. Returns nothing. Creates a file and writes return value of the function return_top_ten_players() and return_average_points() to the file."""

    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    
    outFile = open(path + filename, "w")
    outFile.write("Top 10 Point Leaders in the NHL over the last 5 seasons.\n")
    outFile.write("=============================================================\n\n")
    top_ten_output = return_top_ten_players()
    for i in top_ten_output:
        outFile.write(i + "\n\n")
    outFile.write("The Average Point Total for the Top 10 Players.\n")
    outFile.write("=============================================================\n\n")
    top_ten_average_output = return_average_points()
    outFile.write(top_ten_average_output)
    outFile.close()


def main():
    #search()
    #same_names()
    #other_same_names()
    cur, conn = setUpDatabase('players.db')
    #setup_players_table(cur, conn)
    #setup_players_table(cur, conn)
    #setup_players_table(cur, conn)
    #setup_players_table(cur, conn)
    #set_up_country_table(cur, conn)
    #setup_month_id(cur,conn)
    birth_info_table(cur, conn)
    birth_info_table(cur, conn)
    #birth_info_table(cur, conn)
    #birth_info_table(cur, conn)
    #return_top_ten_players()
    #return_average_points()
    #write_data_to_file("top_ten_player_info.txt")

if __name__ == "__main__":
    main()
    