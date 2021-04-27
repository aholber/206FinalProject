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


def main():
    """Takes no inputs and returns nothing. Selects data from the database to create visualizations that represent our data collected."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/players.db')
    cur = conn.cursor()

    #x-axis
    month_dic = []
    cur.execute('SELECT month FROM Months_id')
    months = cur.fetchall()
    for month in months:
        month_dic.append(month[0])
    print(month_dic)
    
    #y-axis
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

    print(sortguy)

    xlst = []
    for x in sortguy:
        xlst.append(x[0])
    
    ylst = []
    for y in sortguy:
        ylst.append(y[1])


        #if rows[0][0] not in month_dic:
          #  month_dic[rows[0][0]] = 0
        #month_dic[rows[0][0]] += 1
    #print(month_dic)
    #return month_dic


    #months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    values = [6, 8, 11, 9, 16, 7, 15, 7, 10, 14, 7, 11]
    fig = plt.figure(figsize = (10, 5))
    plt.bar(xlst, ylst, color ='maroon', width = 0.3)
    plt.xlabel('Months')
    plt.ylabel('Number of Players')
    plt.title('Number of NHL Players Born Per Month')
    plt.show()




if __name__ == "__main__":
    main()