#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @author: Julien HUBERT

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
import pandas as pd

# Import du dataset apres creation des features de time
data = pd.read_csv('dataV2.csv')

# On supprime les var inutiles
data = data.drop(['datetime','casual','registered'],axis=1)

# Dummies vars for matrix
dataDummies = pd.get_dummies(data, columns=["season","holiday","workingday","weather","hour","day","month",'dow','year'])

# Correlation matrix numerical columns
corrMatt = data[['temp','atemp','humidity','windspeed','doy','count']].corr()
mask = np.array(corrMatt)
mask[np.tril_indices_from(mask)] = False
fig,ax= plt.subplots()
fig.set_size_inches(20,10)
sn.heatmap(corrMatt, mask=mask,vmax=.8, square=True,annot=True)
plt.title("correlation matrix numericals")
plt.show()

# Droites de regression
fig,(ax1,ax2,ax3,ax4) = plt.subplots(ncols=4)
fig.set_size_inches(12, 5)
sn.regplot(x="temp", y="count", data=data,ax=ax1)
sn.regplot(x="humidity", y="count", data=data,ax=ax2)
sn.regplot(x="windspeed", y="count", data=data,ax=ax3)
sn.regplot(x="doy", y="count", data=data,ax=ax4)
plt.title("droites de regression")
plt.show()


# Correlation matrix categorical columns
corrMatt = data[['hour','month','season','year','holiday','workingday','weather','doy','count']].corr()
mask = np.array(corrMatt)
mask[np.tril_indices_from(mask)] = False
fig,ax= plt.subplots()
fig.set_size_inches(20,10)
sn.heatmap(corrMatt, mask=mask,vmax=.8, square=True,annot=True)
plt.title("correlation matrix categoricals")
plt.show()


# Correlation matrix categorical dummies columns 1
corrMatt = dataDummies[['season_1','season_2','season_3','season_4','holiday_0','holiday_1',
                        'count']].corr()
mask = np.array(corrMatt)
mask[np.tril_indices_from(mask)] = False
fig,ax= plt.subplots()
fig.set_size_inches(70,60)
sn.heatmap(corrMatt, mask=mask,vmax=.8, square=True,annot=True)
plt.title("correlation matrix dummies 1")
plt.show()


# Correlation matrix categorical dummies columns 2
corrMatt = dataDummies[['workingday_0','workingday_1','weather_1','weather_2','weather_3',
                        'weather_4','year_2011','year_2012',
                        'count']].corr()
mask = np.array(corrMatt)
mask[np.tril_indices_from(mask)] = False
fig,ax= plt.subplots()
fig.set_size_inches(70,60)
sn.heatmap(corrMatt, mask=mask,vmax=.8, square=True,annot=True)
plt.title("correlation matrix dummies 2")
plt.show()


