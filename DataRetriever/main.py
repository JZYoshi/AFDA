# -*- coding: utf-8 -*-
import glob
import tarfile
import pandas as pd
import os
import zipfile
from data_preparation import group_flight_data_with_conditions

gz_files = []

for filename in glob.glob('./dataset/*.csv.tar'):
    print('extracting ', filename)
    tarObj = tarfile.open(filename)
    for member in tarObj.getmembers():
        if (member.name.endswith('.csv.gz')):
            tarObj.extract(member)
            gz_files.append(member.name)
    tarObj.close()

df = pd.concat((pd.read_csv(f) for f in gz_files))
aircraft_database = pd.read_csv('../aircraft_db/aircraftDatabase.csv')
conditions = {'manufacturericao': 'AIRBUS', 'typecode': r'\bA318\b|\bA319\b|\bA320\b|\bA321\b'}
flight_dict = {}
labels = ['icao24', 'callsign']
new_index = 'time'
group_flight_data_with_conditions(df, flight_dict, labels, new_index, aircraft_database, conditions)
zf = zipfile.ZipFile('test_flight_collection.zip', 'w')
for (k, v) in flight_dict.items():
    filename = './{}_{}.csv'.format(k[0], k[1])
    print('add {} into zip'.format(filename))
    v.to_csv(filename)
    zf.write(filename)
    os.remove(filename)
zf.close()
for file in gz_files:
    os.remove(file)