#!/usr/bin/env python
# coding: utf-8

import sys

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score

sys.path.append("../flight phase on dataset")
from db import *


def pretreatment(database_name, columns_dropped, threshold_nb_flights=100, drop_min_max=True):
    meteo_columns = ["temp_c_descent", "dewpoint_c_descent", "wind_spind_kt_descent", "temp_c_climb", "dewpoint_c_climb", "wind_spind_kt_climb"]
    df = db_to_pandas(filename=database_name)
    df.drop(columns=columns_dropped, inplace=True)
    if drop_min_max:
        df = df[df.columns.drop(list(df.filter(regex="max")))]
        df = df[df.columns.drop(list(df.filter(regex="min")))]

    # drop all lines without airline label
    df.dropna(subset=['airline'], inplace=True)

    # transform label to code
    df["airline"] = df["airline"].astype('category')
    df["airline_cat"] = df["airline"].cat.codes
    df_no_airline = df.drop(columns=['airline'])

    df_no_airline.set_index('flight_id', inplace=True)

    filt_log = df_no_airline['airline_cat'].value_counts() >= threshold_nb_flights
    airline_list_cat = filt_log[filt_log.values].index
    df_filt_log = df_no_airline[df_no_airline['airline_cat'].isin(airline_list_cat)]
    # df_filt_log_meteo = df_filt_log[meteo_columns]
    # df_filt_log_
    # df_filt

    return df_filt_log


def threshold_selection(mad, clf, X_train, X_test, y_train, y_test, accurate, columns, begin=-3, end=3, n_choices=10):
    """
    :param mad:a quoi ca correspond
    :return: une ziqing
    """
    # define the range of threshold

    rg = np.linspace(begin, end, num=n_choices)

    j = 0
    for i in rg:
        j += 1
        sfm = SelectFromModel(clf, threshold=i * mad + np.median(clf.feature_importances_))
        sfm.fit(X_train, y_train)
        X_important_train = sfm.transform(X_train)
        X_important_test = sfm.transform(X_test)
        clf_important = RandomForestClassifier(n_estimators=100, random_state=0, n_jobs=-1)
        clf_important.fit(X_important_train, y_train)
        y_important_pred = clf_important.predict(X_important_test)
        accurate_important = accuracy_score(y_test, y_important_pred)
        print(f'number of evaluation is {j}')
        if accurate_important < accurate:
            break
    sfm = SelectFromModel(clf, threshold=rg[j - 1] * mad + np.median(clf.feature_importances_))
    sfm.fit(X_train, y_train)
    selection = sfm.get_support()
    X_columns = columns[:-1]
    columns_remained = X_columns[selection]
    return columns_remained
