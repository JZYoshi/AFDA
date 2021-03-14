# -*- coding: utf-8 -*-
import glob
import tarfile
import os
from data_preparation import group_flight_data_with_conditions
import dask.dataframe as dd

if __name__=="__main__":
	gz_files = []

	for filename in glob.glob('../data/__tempo_archive/*.csv.tar'):
	    print('extracting ', filename)
	    tarObj = tarfile.open(filename)
	    for member in tarObj.getmembers():
	        if (member.name.endswith('.csv.gz')):
	            tarObj.extract(member)
	            gz_files.append(member.name)
	    tarObj.close()

	df = dd.read_csv('*.csv.gz', blocksize=None)
	aircraft_database = dd.read_csv('../data/aircraftDatabase.csv', dtype={'notes': 'object'})
	conditions = {'manufacturericao': 'AIRBUS', 'typecode': r'\bA318\b|\bA319\b|\bA320\b|\bA321\b'}
	labels = ['icao24', 'callsign']
	new_index = 'time'
	output_dir = '../data/__tempo/'
	group_flight_data_with_conditions(df, labels, new_index, aircraft_database, conditions, output_dir)

	for file in gz_files:
	    os.remove(file)