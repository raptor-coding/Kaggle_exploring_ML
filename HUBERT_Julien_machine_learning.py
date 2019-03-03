#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @author: raptor-coding

import numpy as np
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from math import sqrt

def rmsle(y, y_pred):
	assert len(y) == len(y_pred)
	terms_to_sum = [(math.log(y_pred[i] + 1) - math.log(y[i] + 1)) ** 2.0 for i,pred in enumerate(y_pred)]
	return (sum(terms_to_sum) * (1.0/len(y))) ** 0.5

# Import du dataset apres creation des features de time
data = pd.read_csv('dataV2.csv')

# Pas de donnees manquantes
#msno.matrix(data,figsize=(8,4))

'''
Grace aux precedentes recherches on sait quelles variables ont de l importance ou non
var numeriques : temp, atemp, humidity, windspeed
var categoriques : hour, year, month, season, day, workingday, dow, holiday, weather
var colineraires : temp/atemp et month/season neanmoins il faut garder les 2 dernieres pour ameliorer le RMSE
var importantes : hour, temp, year, month, humidity, weather, season
'''

# On supprime les var inutiles ou colineaires
data = data.drop(['datetime','casual','registered','temp'],axis=1)

# Gestion des variables catégoriques
data = pd.get_dummies(data, columns=['hour','month','year','weather','workingday','dow','season','doy'])
# dummie doy
exclude = ['count']
featuresName = data.columns.difference(exclude).values
Yname = exclude
print(featuresName)
print(Yname)

print(data.shape) # nb lines avant gestion outlier
# Gestion des outliers en Y
data = data[np.abs(data[Yname[0]]-data[Yname[0]].mean())<=(3*data[Yname[0]].std())]
print(data.shape) # nb lines apres gestion outlier

# Split des X et de Y
exclude = ['count']
X = data[featuresName].values
Y = data[Yname].values

print(np.mean(Y))

# Diviser le dataset entre le Training set et le Test set
#from sklearn.model_selection import train_test_split
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Construction du modele de LinearRegression
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
# gestion des predictions negatives
y_pred = np.where(y_pred < 0, 0, y_pred)

# Resultats
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('mesure')
ax.set_ylabel('prediction')
plt.title("LinearRegression model")
plt.show()
print("LinearRegression model")
print('MAE : ',mean_absolute_error(y_test, y_pred))
print('RMSE : ',sqrt(mean_squared_error(y_test,y_pred)))
print('RMSLE : ',rmsle(y_test,y_pred))
print('R2 : ',r2_score(y_test, y_pred))
mape = 100 * (mean_absolute_error(y_test, y_pred) / y_test)
accuracy = 100 - np.mean(mape)
print('Accuracy :', 100+round(accuracy, 2), '%.')

# Construction du modele de ExtraTreesRegressor
from sklearn.ensemble import ExtraTreesRegressor
# Plus d'abres : beaucoup plus de TDC pour une faible amelioration de la MAE
regressor2 = ExtraTreesRegressor(n_estimators=100)
regressor2.fit(X_train, np.ravel(y_train))
y_pred2 = regressor2.predict(X_test)
# gestion des predictions negatives
y_pred2 = np.where(y_pred2 < 0, 0, y_pred2)

# Resultats
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred2)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('reality')
ax.set_ylabel('prediction')
plt.title("ExtraTreesRegressor model")
plt.show()
print("ExtraTreesRegressor model")
print('MAE : ',mean_absolute_error(y_test, y_pred2))
print('RMSE : ',sqrt(mean_squared_error(y_test,y_pred2)))
print('RMSLE : ',rmsle(y_test,y_pred2))
print('R2 : ',r2_score(y_test, y_pred2))
mape = 100 * (mean_absolute_error(y_test, y_pred2) / y_test)
accuracy = 100 - np.mean(mape)
print('Accuracy :', 100+round(accuracy, 2), '%.')

