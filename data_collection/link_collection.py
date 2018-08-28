#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Imports
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import pickle


###Global Variables. Update if running in future
most_recent_season = "2017"


### Set up list of team draft URLs
url_start = 'https://www.pro-football-reference.com/teams/'
teams = {'crd','atl','rav','buf','car','chi','cin','cle','dal','den','det','gnb','htx','clt','jax','kan','sdg','ram','mia','min','nwe','nor','nyj','nyg','rai','phi','pit','sfo','sea','tam','oti','was'}
url_list = list()
all_links = list()

for team in teams:
    url = url_start + team + "/draft.htm"     
    url_list.append(url)
### Get webpage of every player in draft for one team
    response = requests.get(url)
    #print(response.status_code)
    page = response.text
    soup = BeautifulSoup(page,"lxml")

    draft_table_rows = soup.find(id = "draft").find('tbody').find_all('a')
    for row in draft_table_rows:
        if str(row).split("\"")[1].split("/")[1] == "players":
            all_links.append("https://www.pro-football-reference.com" + str(row).split("\"")[1])
    time.sleep(1)

pickle.dump(all_links, open("all_links.pkl","wb"))