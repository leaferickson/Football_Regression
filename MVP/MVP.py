#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 19:44:35 2018

@author: leaferickson
"""

### Imports
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import patsy
import pickle

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error


###Load Data
qbs = pickle.load(open("../data/qbs.pkl","rb"))
qbs.set_index(qbs["Player"], inplace = True)
y = qbs["Rate_x"]
X = qbs[["Att_y", "Cmp_y", "G_y", "Pct", "Int_y", "TD_y", "Yds_y", "Y/A_y", "Rate_y"]]

X_test, X_train, y_test, y_train = train_test_split(X, y, test_size=0.75, random_state=29)


###Linear Modeling

data = X.merge(pd.DataFrame(y), left_index = True, right_index = True)
sns.pairplot(data, size = 1.2, aspect=1.5);

lm = smf.ols('Rate_x ~ Rate_y + Pct + Cmp_y + TD_y + Int_y + G_y', data = data)
most_naive_model = lm.fit()
most_naive_model.summary()

plt.scatter(most_naive_model.predict(X_test), y_test)
plt.title("Predicted vs. Actual Passer Rating", y = 1.06, fontsize = 15)
plt.suptitle("Using test data. Based on QB's college stats", y = .93)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig('first_model')



plt.scatter(X["Pct"],y)
plt.title("College Completion Percentage vs. Pro Passer Rating")
plt.xlabel("Colleg Comp %")
plt.ylabel("Pro Rating")
most_naive_model.predict(X["Pct"])
plt.plot(X["Pct"],y,'g--')

lr = LinearRegression()
lr.fit(X,y)
lr.resid.plot(style='o', figsize=(12,8));
lr.mean_squared_error

