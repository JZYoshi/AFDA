#!/usr/bin/env python
# coding: utf-8


## importations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from os import listdir

## functions
def calculate_descriptor(phase):
    duration = int(-phase['time'].iloc[0]+ phase['time'].iloc[-1])
    avg_spd = phase['velocity'].mean()
    std_spd = phase['velocity'].std()
    vertrate_avg_spd = phase['vertrate'].mean()
    vertrate_std_spd = phase['vertrate'].std()
    delta_h = phase['geoaltitude'].iloc[-1] - phase['geoaltitude'].iloc[0]
    max_spd = phase['velocity'].max()
    min_spd = phase['velocity'].min()
    max_vertrate_spd = phase['vertrate'].max()
    min_vertrate_spd = phase['vertrate'].min()
    del phase
    return locals()

## main

path_to_dataset = "./test_flight_collection_with_phase/"
result_dir = "./test_flight_collection_descriptors/"
os.mkdir(result_dir)

list_file_name = listdir(path_to_dataset)

for file_name in list_file_name:
    print(file_name)
    df = pd.read_csv(path_to_dataset+file_name)
    df.fillna(value={'phase':'NA'},inplace=True)

    climb = df[df['phase']=='CL']
    if not climb.empty:
        desc_climb = calculate_descriptor(climb)
    else:
        desc_climb={}

    cruise = df[df['phase']=='CR']
    if not cruise.empty:
        desc_cruise = calculate_descriptor(cruise)
        desc_cruise['mean_altitude'] = cruise['geoaltitude'].mean()
        desc_cruise['std_altitude'] = cruise['geoaltitude'].std()
    else:
        desc_cruise={}


    descent = df[df['phase']=='DE']
    if not descent.empty:
        desc_descent = calculate_descriptor(descent)
    else:
        desc_descent={}



    descriptor = {'climb':desc_climb, 'cruise':desc_cruise, 'descent':desc_descent}


    with open(result_dir+os.path.splitext(file_name)[0]+'.json', 'w') as my_file:
        json.dump(descriptor, my_file)

