import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib

## df = pd.read_csv("Melbourne_housing_FULL_test.csv")
df = pd.read_csv("Melbourne_housing_FULL.csv")

# Normalise data(transfer different feature of string type into orderd number)
enc = LabelEncoder()
df.iloc[:,0] = enc.fit_transform(df.iloc[:,0])
df.iloc[:,3] = enc.fit_transform(df.iloc[:,3])

## Data cleasing, remove row which contains null
#df2 = df[df.Price.notnull()]
#df2 = df2[df2.Distance.notnull()]
#df2 = df2[df2.Car.notnull()]
#df2 = df2[df2.BulidingArea.notnull()]
#df2 = df2[df2.YearBuilt.notnull()]
#df2['year'] = (2018 - df2.YearBuilt)
#df2 = df2[~df2['BulidingArea'].isin(['0'])]

# Data cleasing, for some columns replace none value with mean value
impute_value_price = df['Price'].mean()
df['Price'] = df['Price'].fillna(impute_value_price)

impute_value_car = df['Car'].mean()
df['Car'] = df['Car'].fillna(impute_value_car)

impute_value_area = df['BuildingArea'].mean()
df['BuildingArea'] = df['BuildingArea'].fillna(impute_value_area)

## remove some row with none value
#df2 = df[df.Price.notnull()]
df2 = df[df.Distance.notnull()]
#df2 = df2[df2.Car.notnull()]
#df2 = df2[df2.BulidingArea.notnull()]
df2 = df2[df2.YearBuilt.notnull()]
df2['year'] = (2018 - df2.YearBuilt)

# Select columns(features) which are highly related to price to train the model
X = df2.iloc[:,[0,2,3,8,12,14,21]]
Y = df2.Price
X = pd.get_dummies(X, drop_first=True)

## linear regression
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.25)
linear = LinearRegression()
linear.fit(X_train, Y_train)

# print(cross_val_score(linear, X_train, Y_train, cv=5))
# [0.52493576 0.51610201 0.48970882 0.52427755 0.38024456]

## prediction
pred = linear.predict(X_test)
# score = r2_score(Y_test,pred) 
# 0.5269530680297595
# rmse = np.sqrt(mean_squared_error(Y_test, pred)) 
# 462482.2032009657
# Score looks good

# import model file
## get the model
joblib.dump(linear, "mel_hp.ml")
