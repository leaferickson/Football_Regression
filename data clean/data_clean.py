#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 15:00:38 2018

@author: leaferickson
"""

### Imports
import pandas as pd
import numpy as np
import pickle


###Global Variables. Update if running in future



###Cleaning Data
pro_qbs = pickle.load(open("../data/pro_qbs.pkl","rb"))
pro_rbs = pickle.load(open("../data/pro_rbs.pkl","rb"))
pro_wrs = pickle.load(open("../data/pro_wrs.pkl","rb"))
college_qbs = pickle.load(open("../data/college_qbs.pkl","rb"))
college_rbs = pickle.load(open("../data/college_rbs.pkl","rb"))
college_wrs = pickle.load(open("../data/college_wrs.pkl","rb"))


###Get data down to relevant columns
def drop_unnecesarry_columns(df, col_slice_start_to_keep, col_slice_end_to_keep):
    temp = df.iloc[:,col_slice_start_to_keep:col_slice_end_to_keep]
    temp["Player"] = df["Player"]
    return temp

college_rbs = drop_unnecesarry_columns(college_rbs,0,10)
college_wrs = drop_unnecesarry_columns(college_wrs,0,10)


college_qbs.drop([11,15], axis = 1, inplace = True)
pro_qbs.drop([0,1,2,3,4,16,18,19,22,23,24,25,26,27,28,29,30,31], axis = 1, inplace = True)
pro_rbs.drop([0,1,2,3,4,10,14,15,16,17,18,19,20,21,22,26,27,28,29], axis = 1, inplace = True)
pro_wrs.drop([0,1,2,3,4,12,15,16,17,18,19,20,21,22,26,27,28,29], axis = 1, inplace = True)


###Make Row 1 the header, not row 1
def clean_columns(df):
    df.columns = df.iloc[0]
    df.columns.values[-1] = 'Player'
    return df

def clean_college_columns(df):
    df = df.reset_index(drop = True)
    df = df.drop(0)
    df["Year"] = df["Year"].str.replace('\W', '')
    return df

dfs_list = list()
dfs_list.append(college_qbs)
dfs_list.append(college_rbs)
dfs_list.append(college_wrs)
dfs_list.append(pro_qbs)
dfs_list.append(pro_rbs)
dfs_list.append(pro_wrs)

for df in dfs_list:
    df = clean_columns(df)



college_qbs = clean_college_columns(college_qbs)
college_rbs = clean_college_columns(college_rbs)
college_wrs = clean_college_columns(college_wrs)


###Final Year Data
qb_names = set(college_qbs['Player'])
rb_names = set(college_rbs['Player'])
wr_names = set(college_wrs['Player'])


def get_final_college_year(df, my_set):
    df = df[(df["Year"] != "Career")]
    toReturn = pd.DataFrame()
    for name in my_set:
        players_rows = df[(df["Player"] == name)]
        toReturn = toReturn.append(players_rows[(players_rows["Year"] == players_rows["Year"].max())])
    return toReturn


#col_qbs_years = col_qbs[(col_qbs["Year"] != "Career")]
senior_qbs = get_final_college_year(college_qbs,qb_names)
senior_rbs = get_final_college_year(college_rbs,rb_names)
senior_wrs = get_final_college_year(college_wrs,wr_names)
college_qb_career = college_qbs[(college_qbs["Year"] == "Career")]
college_rb_career = college_rbs[(college_rbs["Year"] == "Career")]
college_wr_career = college_wrs[(college_wrs["Year"] == "Career")]



#####THE SCRIPT DIVERGES HERE!!
###Runs for only Senior/final year stats as it stands
###For Total College stats, uncomment out below
qbs = senior_qbs[["Year","Conf", "Player"]]
college_qb_career = college_qb_career.merge(qbs, on = 'Player')
rbs = senior_rbs[["Year","Conf", "Player"]]
college_rb_career = college_rb_career.merge(rbs, on = 'Player')
wrs = senior_wrs[["Year","Conf", "Player"]]
college_wr_career = college_wr_career.merge(wrs, on = 'Player')
    



# There are a tiny amount of repeats, but that's ok for now. MVP time
qbs = pro_qbs.merge(college_qb_career, on = 'Player')
rbs = pro_rbs.merge(college_rb_career, on = 'Player')
wrs = pro_wrs.merge(college_wr_career, on = 'Player')
#Drop row we got headers from, nas, duplicates
qbs = qbs.drop_duplicates()
rbs = rbs.drop_duplicates()
wrs = wrs.drop_duplicates()


#qbs2 = qbs[(qbs["Cmp_x"] >= 100) & (qbs["Cmp_y"] >= 50)]

###Add Year column for senior years
###Format columns, and save cleaned Data
qbs[["Year","Cmp_x", "Cmp_y", "G_x", "GS", "Att_x", "Cmp%", "Yds_x", "TD_x", "Rate_x", "Rate_y", "TD_y", "Int_y", "Yds_y", "Att_y", "Cmp_y", "Pct", "Y/A_y"]] = qbs[["Year_y","Cmp_x", "Cmp_y", "G_x", "GS", "Att_x", "Cmp%", "Yds_x", "TD_x", "Rate_x", "Rate_y", "TD_y", "Int_y", "Yds_y", "Att_y", "Cmp_y", "Pct", "Y/A_y"]].apply(pd.to_numeric)
rbs[["Year","G_x","Rush","Yds_x","TD_x","Fmb","Att","Yds_y","Avg","TD_y"]] = rbs[["Year_y","G_x","Rush","Yds_x","TD_x","Fmb","Att","Yds_y","Avg","TD_y"]].apply(pd.to_numeric)
wrs[["Year","G_x","Yds_x","TD_x","Rec_x","Fmb","Y/G","Rec_y","TD_y","Avg","Yds_y"]] = wrs[["Year_y","G_x","Yds_x","TD_x","Rec_x","Fmb","Y/G","Rec_y","TD_y","Avg","Yds_y"]].apply(pd.to_numeric)
qbs = qbs.dropna()
rbs = rbs.dropna()
wrs = wrs.dropna()


rbs = rbs[(rbs["Yds_x"] >= rbs["TD_x"])]
rbs = rbs[(rbs["TD_x"] <= 164)]
qbs = qbs[(qbs["Cmp_x"] >= 30)]
wrs = wrs[(wrs["Rec_y"] >= 15)]
rbs = rbs[(rbs["Rush"] >= 15)]



###Add Categorical Data: Conference
big_conference = {"AAWU", "American", "ACC", "Big 12", "Big 8", "Big Ten", "Big East", "Pac-12", "Pac-10", "Pac-8", "PCC", "SEC", "SWC", "Ind"}

def add_conference_move_year(df):
    ####Uncomment this back in for Senior Years, and comment out the rest of function
#    year = df["Year"]
#    df = df.drop("Year", axis = 1)
#    df["Year"] = year
    big_con_list = list()
    for index, row in df.iterrows():
        big_con_list.append(row["Conf_y"] in big_conference)
    df = df.drop("Conf_y", axis = 1)
    df["Conf"] = big_con_list
    return df

qbs = add_conference_move_year(qbs)
rbs = add_conference_move_year(rbs)
wrs = add_conference_move_year(wrs)

###Comment this out when doing senior year only
qbs = qbs.drop("Year_y", axis = 1)
rbs = rbs.drop("Year_y", axis = 1)
wrs = wrs.drop("Year_y", axis = 1)


# Change dump names to senior when doing senior year
pickle.dump(qbs, open("../data/qbs_career.pkl","wb"))
pickle.dump(rbs, open("../data/rbs_career.pkl","wb"))
pickle.dump(wrs, open("../data/wrs_career.pkl","wb"))