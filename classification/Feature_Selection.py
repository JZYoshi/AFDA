#!/usr/bin/env python
# coding: utf-8

# # Feature Selection



from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score
import numpy as np
from scipy.stats import median_abs_deviation
import sys
sys.path.append("../flight phase on dataset")
import db

threshold_nb_flights = 10
database_name = 'descriptors_meteo.db'



df = db.db_to_pandas(filename = database_name)
df.drop(columns=['icao', 'icao_airline', 'duration_descent', 'duration_cruise', 'duration_climb', 'airport_climb', 'airport_descent'],inplace=True)
df.dropna(subset = ['airline'], inplace = True)
df["airline"] = df["airline"].astype('category')
df["airline_cat"]=df["airline"].cat.codes
df_noairline = df.drop(columns=['airline'])
df_noairline.set_index('flight_id',inplace=True)
columns = df_noairline.columns
filt_10log = df_noairline['airline_cat'].value_counts()>=threshold_nb_flights
airline_list_cat = filt_10log[filt_10log.values==True].index
df_filt_10log = df_noairline[df_noairline['airline_cat'].isin(airline_list_cat)]
feature_selection_df = df_filt_10log.dropna()
X = feature_selection_df.iloc[:,:-1]
y = feature_selection_df.loc[:,["airline_cat"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
clf = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
accurate = accuracy_score(y_test, y_pred)

mad = median_abs_deviation(clf.feature_importances_)


def threshold_selection(begin=-3, end=3, n_choices=10):
# define the range of threshold
    rg = np.linspace(begin, end, num=n_choices)
    
    j=0
    for i in rg:
        j+=1
        sfm = SelectFromModel(clf, threshold=i*mad+np.median(clf.feature_importances_))
        sfm.fit(X_train, y_train)
        X_important_train = sfm.transform(X_train)
        X_important_test = sfm.transform(X_test)
        clf_important = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)
        clf_important.fit(X_important_train, y_train)
        y_important_pred = clf_important.predict(X_important_test)
        accurate_important = accuracy_score(y_test, y_important_pred)
        print(i)
        if accurate_important < accurate:
            break
    sfm = SelectFromModel(clf, threshold=rg[j-1]*mad+np.median(clf.feature_importances_))
    sfm.fit(X_train, y_train)
    selection = sfm.get_support()
    X_columns = columns[:-1]
    columns_remained = X_columns[selection]
    return columns_remained
