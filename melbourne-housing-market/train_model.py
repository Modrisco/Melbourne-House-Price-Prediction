import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib

df = pd.read_csv("Melbourne_housing_FULL.csv")
enc = LabelEncoder()
df.iloc[:,0] = enc.fit_transform(df.iloc[:,0])
df.iloc[:,3] = enc.fit_transform(df.iloc[:,3])

# Data cleasing, remove row which contains null
df2 = df[df.Price.notnull()]
df2 = df2[df2.Distance.notnull()]
df2 = df2[df2.Car.notnull()]
df2 = df2[df2.Landsize.notnull()]
df2 = df2[df2.YearBuilt.notnull()]
df2['year'] = (2018 - df2.YearBuilt)
df2 = df2[~df2['Landsize'].isin(['0'])]

# Select columns which are highly related to price
X = df2.iloc[:,[0,2,3,8,12,13,21]]
Y = df2.Price
X = pd.get_dummies(X, drop_first=True)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.25)
linear = LinearRegression()
linear.fit(X_train, Y_train)

# print(cross_val_score(linear, X_train, Y_train, cv=5))
# [0.35948662 0.37590135 0.39705553 0.45022753 0.42608876]

pred = linear.predict(X_test)
# score = r2_score(Y_test,pred) 
# 0.4360122355807299
# rmse = np.sqrt(mean_squared_error(Y_test, pred)) 
# 516187.90649574023

# import model file
joblib.dump(linear, "mel_hp.ml")