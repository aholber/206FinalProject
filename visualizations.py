import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json
from bettercombined import return_first_three_months



def main():
    """Takes no inputs and returns nothing. Selects data from the database to create visualizations that represent our data collected."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/players.db')
    cur = conn.cursor()

   
    #1!!!!!
    #first visualization info
    month_dic = {}
    cur.execute('SELECT birth_month FROM Birthdays')
    months = cur.fetchall()
    
    for month in months:
        cur.execute('SELECT month FROM Months_id WHERE id = ? ', (month))
        rows = cur.fetchall()

        if rows[0][0] not in month_dic:
            month_dic[rows[0][0]] = 0
        month_dic[rows[0][0]] += 1

    sortguy = (sorted(month_dic.items(), key = lambda x: x[1]))


    #x-axis
    xlst_graph1 = []
    for x in sortguy:
        xlst_graph1.append(x[0])
    
    #y-axis
    ylst_graph1 = []
    for y in sortguy:
        ylst_graph1.append((y[1]/121))

    #2!!!!!
    #second visualization info
    country_dic = {}
    cur.execute('SELECT birth_place FROM Birthdays')
    countries = cur.fetchall()
    
    for country in countries:
        cur.execute('SELECT country FROM Countries WHERE id = ? ', (country))
        rows = cur.fetchall()

        if rows[0][0] not in country_dic:
            country_dic[rows[0][0]] = 0
        country_dic[rows[0][0]] += 1

    sortguy = (sorted(country_dic.items(), key = lambda x: x[1]))

    #x-axis
    xlst_graph2 = []
    for x in sortguy:
        xlst_graph2.append(x[0])
    
    #y-axis
    ylst_graph2 = []
    for y in sortguy:
        ylst_graph2.append((y[1]/121))

    
    #3!!!!!
    #third visualization info
    pie_guy = return_first_three_months(cur, conn)

    #visualization 1 - bar graph / month
    fig = plt.figure(figsize = (10, 5))
    plt.bar(xlst_graph1, ylst_graph1, color ='maroon', width = 0.3)
    plt.xlabel('Months')
    plt.ylabel('Percent of Players')
    plt.title('Percent of NHL Players Born Per Month')
    plt.show()

    #visualization 2 - bar graph / country
    fig = plt.figure(figsize = (10, 5))
    plt.bar(xlst_graph2, ylst_graph2, color ='blue', width = 0.3)
    plt.xlabel('Countries')
    plt.ylabel('Percent of Players')
    plt.title('Percent of NHL Players Born Per Country')
    plt.show()

    #visualization 3 - pie chart / 
    y = np.array([pie_guy[0],pie_guy[1]])
    mylabels = ["Jan, Feb, Mar", "Last 9 Months"]
    myexplode = [0.2, 0]

    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%".format(pct, absolute)
    
    plt.pie(y, autopct = lambda pct: func(pct, y), labels = mylabels, shadow = True, explode = myexplode)
    plt.title("Percent of NHL Leaders Born in First Three Months")
    plt.show() 




if __name__ == "__main__":
    main()