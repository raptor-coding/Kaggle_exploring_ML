# Kaggle_exploring_ML


Données historiques de locations de vélos :
- datetime ­ date et heure du relevé
- season ­ 1 = printemps , 2 = été, 3 = automne, 4 = hiver
- holiday – indique si le jour est un jour de vacances scolaires
- workingday ­ indique si le jour est travaillé (ni week­end ni vacances)
- weather ­ 1: Dégagé à nuageux, 2 : Brouillard, 3 : Légère pluie ou neige, 4 : Fortes averses ou neiges
- temp – température en degrés Celsius
- atemp – température ressentie en degrés Celsius
- humidity – taux d’humidité
- windspeed – vitesse du vent
- casual ­ nombre de locations d’usagers non abonnés
- registered – nombre de locations d’usagers abonnés
- count – nombre total de locations de vélos


Feature Engineering :
création de features depuis le datetime -> extraction de l'heure, du jour de la semaine, du jour de mois, du jour de l'année, du mois et de l'année.

Data Exploration :
Données numériques -> A partir du dataset V2 plot avec matplotlib de toutes les dimensions sur le nombre de vélo loués (moyenne des observations pour avoir un point par valeur de X).
Données catégorielles (workingDay, holiday, season, dayOfWeek, weather) -> On les place sur les heures de la journée pour visualiser les tendances à l'échelle des heures.
En sortie du script des plot et un tableau de corrélation.

Matrices de corrélations seaborn :
Matrice de corrélation pour données numériques.
Matrice de corrélation pour données catégoriques.

Machine Learning :
Suppression variable colinéaire, dummies variables, gestion des données abérrantes, training/test set, feature scaling, modèle LinearRegression et modèle ExtraTreesRegressor -> résulat MAE, RMSE, RMSLE et R2
