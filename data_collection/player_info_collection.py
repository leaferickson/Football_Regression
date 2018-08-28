#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Imports
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import pickle

###Make table headers for RB's,WR's, and QB's, both pro and college
all_links = pickle.load(open("all_links.pkl","rb"))
def get_table_header(link, pro_qb):
    if pro_qb == True:
        headerRows = 0
    else:
        headerRows = 1
    response = requests.get(link)
    page = response.text
    soup = BeautifulSoup(page,"lxml")   
    header_data = list()
    for element in soup.find('table').find('thead').find_all('tr')[headerRows].text.split("\n")[1:-1]:
        header_data.append(element)
    header_data.append("Player")
    return pd.DataFrame.transpose(pd.DataFrame(header_data))

pro_rbs = get_table_header("https://www.pro-football-reference.com/players/E/ElliEz00.htm", False)
pro_wrs = get_table_header("https://www.pro-football-reference.com/players/J/JeffAl00.htm", False)
pro_qbs = get_table_header("https://www.pro-football-reference.com/players/P/PalmCa00.htm", True)
college_rbs = get_table_header("https://www.sports-reference.com/cfb/players/ezekiel-elliott-1.html", False)
college_wrs = get_table_header("https://www.sports-reference.com/cfb/players/alshon-jeffery-1.html", False)
college_qbs = get_table_header("https://www.sports-reference.com/cfb/players/carson-palmer-1.html", False)



###Get info of every player
def put_data_in_table(data, position, college = False):
    if college == False:
        if position == "QB":
            pro_qbs = pro_qbs.append(data)
        if position == "RB":
            pro_rbs = pro_rbs.append(data)
        if position == "WR":
            pro_wrs = pro_wrs.append(data)            
    else:
        if position == "QB":
            college_qbs = college_qbs.append(data)
        if position == "RB":
            college_rbs = college_rbs.append(data)
        if position == "WR":
            college_wrs = college_wrs.append(data)
            
            
for link in all_links:
    time.sleep(0.2)
    response = requests.get(link)
    page = response.text
    soup = BeautifulSoup(page,"lxml")
    
    #Filter for only QB's, RB's, and WR's
    paragraph_tags = soup.find(id = "meta").find_all('p')[1]
    position = paragraph_tags.text.strip()
    position = position[10:12]
    college_table = ""
    if position == "RB":
        college_table = "passing"
    if position == "RB":
        college_table = "rushing"
    if position == "WR":
        college_table = "receiving"
    try:
        if position == "RB" or position == "WR" or position == "QB":
            #Scrape Pro Stats for the slected player
            if soup.find('table').find('tbody').find_all('tr')[-1].find('a').text != most_recent_season:    #Exclude the most recent year
                footer = list()
                footer.append("Career")
                footer.append("")
                footer_texts = soup.find('table').find('tfoot').find('tr').find_all('td')
                for element in footer_texts:
                    footer.append(element.text)
                pro_stats = pd.DataFrame.transpose(pd.DataFrame(footer))
                pro_stats["Player"] = soup.find(id = "meta").find("h1").text
                put_data_in_table(pro_stats, position, False)
                #Get link to college stats for the player
                player_html_a = soup.find(id = "meta").find_all('a')
                for a_tag in player_html_a:
                    college_links = str(a_tag).split("\"")[1]
                    if college_links[0:18] == "https://www.sports":
                        college_link = (college_links)
                        #Get college stats
                        response = requests.get(college_link)
                        page = response.text
                        soup = BeautifulSoup(page,"lxml")
                        player_data = list()
                        for row in soup.find(id = college_table).find('tbody').find_all('tr'):
                            year_data = list()
                            year_data.append(row.find('th').text)
                            for td in row.find_all('td'):
                                year_data.append(td.text)
                            player_data.append(year_data)
                        footer = list()
                        footer.append("Career")
                        footer_texts = soup.find(id = college_table).find('tfoot').find('tr').find_all('td')
                        for element in footer_texts:
                            footer.append(element.text)
                        player_data.append(footer)
                        college_data = pd.DataFrame(player_data)
                        college_data["Player"] = pro_stats["Player"][0]
                        put_data_in_table (college_data, position, True)  
    except:
        pass
    
pickle.dump(pro_qbs, open("../data/pro_qbs.pkl","wb"))
pickle.dump(pro_rbs, open("../data/pro_rbs.pkl","wb"))
pickle.dump(pro_wrs, open("../data/pro_wrs.pkl","wb"))
pickle.dump(college_qbs, open("../data/college_qbs.pkl","wb"))
pickle.dump(college_rbs, open("../data/college_rbs.pkl","wb"))
pickle.dump(college_wrs, open("../data/college_wrs.pkl","wb"))
