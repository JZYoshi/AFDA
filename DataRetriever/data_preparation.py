# -*- coding: utf-8 -*-
import pandas as pd

def group_flight_data_with_conditions(df, flight_dict, labels, new_index, aircraft_database, conditions):
    """
    To split the raw flight dataframe into new dataframes based on the given *labels*, and set the given *new_index*
    as their index. It is possible to filter the dataframes by the given *conditions* that should be related to 
    the aircraft of the flight. *aircraft_database_df* should be a dataframe of the aircraft database given
    by the OpenSky Network <https://opensky-network.org/datasets/metadata/>_, and it contains all the info of aircrafts.
    The result is stored in *flight_dict*. 

    :param df: a Pandas dataframe containing raw flight data

    :param flight_dict: an empty dictionary used to store results. Key: labels, Value: new dataframe

    :param labels: a list of strings that should also be part of column labels of the raw dataframe

    :param new_index: a string that will be the new index of the new dataframes, should also be one of column labels of the raw dataframe

    :param aircraft_database: a dataframe of the aircraft database provided by OpenSky Network <https://opensky-network.org/datasets/metadata/>_

    :param conditions: a dict whose keys are part of the *aircraft_database* labels, and whose values are string or regex  
    """
    ad_id = []
    columns = list(aircraft_database.columns)
    df = df.dropna(subset=labels)
    for i, label in enumerate(labels):
        df[label] = df[label].str.strip()
        df.drop(df[df[label].str.len() == 0].index, inplace=True)
        if label in columns:
            ad_id.append((i, label))
    df_groupby = df.groupby(labels)
    for group_key in df_groupby.groups.keys():
        not_satisfied = False
        id_dict = dict((t[1], [group_key[t[0]]]) for t in ad_id)
        entry = aircraft_database[aircraft_database[id_dict.keys()].isin(id_dict).all(1)]
        if (entry.empty):
            continue
        for (k, v) in conditions.items():
            if not all(entry[k].str.match(v, na=False)):
                not_satisfied = True
                break
        if not_satisfied:
            continue
        print('get one')
        group = df_groupby.get_group(group_key)
        group.drop(labels, axis=1, inplace=True)
        group.set_index(new_index, inplace=True)
        if group_key in flight_dict:
            flight_dict[group_key] = pd.concat([flight_dict.get(group_key), group])
        else:
            flight_dict[group_key] = group 
            