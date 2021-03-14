# -*- coding: utf-8 -*-

def group_flight_data_with_conditions(df, labels, new_index, aircraft_database, conditions, output_dir):
    """
    To split the raw flight dataframe into new dataframes based on the given *labels*, and set the given *new_index*
    as their index. It is possible to filter the dataframes by the given *conditions* that should be related to 
    the aircraft of the flight. *aircraft_database_df* should be a dataframe of the aircraft database given
    by the OpenSky Network <https://opensky-network.org/datasets/metadata/>_, and it contains all the info of aircrafts.
    The dataframes will be written to csv files named by *labels* in *output_dir*. 

    :param df: a Pandas dataframe containing raw flight data

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
        df = df[df[label].str.len() > 0]
        if label in columns:
            ad_id.append((i, label))
    df_groupby = df.groupby(labels)

    def filter_and_register(group, ad_id, labels, aircraft_database, conditions, output_dir):
        group_key = group[labels].head(1).values[0].tolist()
        not_satisfied = False
        id_dict = dict((t[1], [group_key[t[0]]]) for t in ad_id)
        entry = aircraft_database[aircraft_database[id_dict.keys()].isin(id_dict).all(1)]
        if not entry.empty:
            for (k, v) in conditions.items():
                if not all(entry[k].str.match(v, na=False)):
                    not_satisfied = True
                    break
        if not not_satisfied:
            group = group.drop(labels, axis=1).set_index(new_index)
            import os
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            filename = output_dir + '{}_{}.csv'.format(group_key[0], group_key[1])
            group.to_csv(filename)
        return 0
    
    df_groupby.apply(filter_and_register, ad_id, labels, aircraft_database, conditions, output_dir, meta=('int')).compute()
    
            