#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @author: Julien HUBERT

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import pandasql as pdsql

# Import du dataset apres creation des features de time
data = pd.read_csv('dataV2.csv')

'''
On donne du sens aux donnees categoriques workingday/holiday/season/dayOfWeek/weather
# en les plaçant sur les heures (granularite la plus fine du dataset) pour visualiser les tendances
'''
# workingDay plot
pysql = lambda q: pdsql.sqldf(q, globals())
workingDay = [0,1]
workingDayLabel = ['non working day','working day']
workingDayColor = ['red','green']
patches = []
for i in range(0,len(workingDay)):
    sql = 'SELECT hour, avg(count) as meanLoc FROM data WHERE workingday='+str(workingDay[i])+' GROUP BY hour;'
    df1 = pysql(sql)
    plt.plot(df1['hour'],df1['meanLoc'],color=workingDayColor[i])
    patches.append(mpatches.Patch(color=workingDayColor[i], label=workingDayLabel[i]))
plt.legend(handles=patches)
plt.xlabel("hour")
plt.ylabel("meanLoc")
plt.title("locations by hours over working/non working day")
plt.show()
plt.clf()

# holiday plot
holiday = [0,1]
holidayLabel = ['non holiday','holiday']
holidayColor = ['red','green']
patches = []
for i in range(0,len(holiday)):
    sql = 'SELECT hour, avg(count) as meanLoc FROM data WHERE holiday='+str(holiday[i])+' GROUP BY hour;'
    df1 = pysql(sql)
    plt.plot(df1['hour'],df1['meanLoc'],color=holidayColor[i])
    patches.append(mpatches.Patch(color=holidayColor[i], label=holidayLabel[i]))
plt.legend(handles=patches)
plt.xlabel("hour")
plt.ylabel("meanLoc")
plt.title("locations by hours over holiday/non holiday")
plt.show()
plt.clf()

# season plot
season = [1,2,3,4]
seasonLabel = ['spring','summer','fall','winter']
seasonColor = ['green','red','orange','blue']
patches = []
for i in range(0,len(season)):
    sql = 'SELECT hour, avg(count) as meanLoc FROM data WHERE season='+str(season[i])+' GROUP BY hour;'
    df1 = pysql(sql)
    plt.plot(df1['hour'],df1['meanLoc'],color=seasonColor[i])
    patches.append(mpatches.Patch(color=seasonColor[i], label=seasonLabel[i]))
plt.legend(handles=patches)
plt.xlabel("hour")
plt.ylabel("meanLoc")
plt.title("locations by hours over season")
plt.show()
plt.clf()

# dayOfWeek plot
pysql = lambda q: pdsql.sqldf(q, globals())
DoW = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
colorDoW = ['green','red','orange','blue','navy','salmon','yellow','cyan']
patches = []
for i in range(0,len(DoW)):
    sql = 'SELECT hour, avg(count) as meanLoc FROM data WHERE dow="'+DoW[i]+'" GROUP BY hour;'
    df1 = pysql(sql)
    plt.plot(df1['hour'],df1['meanLoc'],color=colorDoW[i])
    patches.append(mpatches.Patch(color=colorDoW[i], label=DoW[i]))
plt.legend(handles=patches)
plt.xlabel("hour")
plt.ylabel("meanLoc")
plt.title("locations by hours over day of week")
plt.show()
plt.clf()

# weather plot
weather = [1,2,3,4]
weatherLabel = ['clear','frog','rain/snow','heavy rain/snow']
weatherColor = ['green','orange','red','black']
patches = []
for i in range(0,len(weather)):
    sql = 'SELECT hour, avg(count) as meanLoc FROM data WHERE weather='+str(weather[i])+' GROUP BY hour;'
    df1 = pysql(sql)
    plt.plot(df1['hour'],df1['meanLoc'],color=weatherColor[i])
    patches.append(mpatches.Patch(color=weatherColor[i], label=weatherLabel[i]))
plt.legend(handles=patches)
plt.xlabel("hour")
plt.ylabel("meanLoc")
plt.title("locations by hours over weather condition")
plt.show()
plt.clf()

# Maintenant on parcours les donnees numeriques
data = data.drop(['datetime','casual','registered'],axis=1)

# Superposition de temp et atemp
sql = 'SELECT temp, avg(count) as meanLoc FROM data GROUP BY temp;'
df1 = pysql(sql)
plt.plot(df1['temp'],df1['meanLoc'],color='green')
sql = 'SELECT atemp, avg(count) as meanLoc FROM data GROUP BY atemp;'
df1 = pysql(sql)
plt.plot(df1['atemp'],df1['meanLoc'],color='red')
patches = []
patches.append(mpatches.Patch(color='green', label='temp'))
patches.append(mpatches.Patch(color='red', label='atemp'))
plt.legend(handles=patches)
plt.xlabel("temp")
plt.ylabel("count")
plt.title("locations over temp/atemp")
plt.show()
plt.clf()

# Comparaison sur les annees à l echelle des mois
pysql = lambda q: pdsql.sqldf(q, globals())
years = [2011,2012]
colorYears = ['yellow','cyan']
patches = []
for i in range(0,len(years)):
    sql = 'SELECT month, avg(count) as meanLoc FROM data WHERE year="'+str(years[i])+'" GROUP BY month;'
    df1 = pysql(sql)
    plt.plot(df1['month'],df1['meanLoc'],color=colorYears[i])
    patches.append(mpatches.Patch(color=colorYears[i], label=years[i]))
plt.legend(handles=patches)
plt.xlabel("month")
plt.ylabel("meanLoc")
plt.title("locations by month over years")
plt.show()
plt.clf()


# On get les noms des vars de X et le nom de Y pour la boucle
exclude = ['count']
XNames = data.columns.difference(exclude).values
Yname = exclude[0]
print(XNames)
print(Yname)

# On donne un ordre aux jours de la semaine pour constater ou non une tendance a l'echelle de le semaine
data.loc[data['dow'] == 'Monday', ['dow']] = 0
data.loc[data['dow'] == 'Tuesday', ['dow']] = 1
data.loc[data['dow'] == 'Wednesday', ['dow']] = 2
data.loc[data['dow'] == 'Thursday', ['dow']] = 3
data.loc[data['dow'] == 'Friday', ['dow']] = 4
data.loc[data['dow'] == 'Saturday', ['dow']] = 5
data.loc[data['dow'] == 'Sunday', ['dow']] = 6

correlationArray = [[]]
# Plot du dataset dimension par dimension
for i in range(0,len(XNames)):
    corr = data[Yname].corr(data[XNames[i]])
    correlationArray.append([XNames[i], corr])
    print('correlation between '+Yname+' and '+XNames[i]+' : ',corr)
    plt.plot(data.groupby(XNames[i])[Yname].mean(),color="orange") # Moyenne des locations par dimension
    plt.xlabel(XNames[i])
    plt.ylabel(Yname)
    plt.title(("locations over "+XNames[i]))
    plt.show()

correlationArray.pop(0)
correlationArray = sorted(correlationArray,key=lambda x:(x[1]),reverse=True)
# Tableau de correlation
for feature in correlationArray:
    print(feature)

