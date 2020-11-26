#!/usr/bin/env python
# coding: utf-8


## importations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from os import listdir
from db import get_db, init_db

## functions
def calculate_descriptor(phase):
    duration = int(-phase['time'].iloc[0]+ phase['time'].iloc[-1])
    avg_spd = phase['velocity'].mean()
    std_spd = phase['velocity'].std()
    vertrate_avg_spd = phase['vertrate'].mean()
    vertrate_std_spd = phase['vertrate'].std()
    delta_h = phase['baroaltitude'].iloc[-1] - phase['baroaltitude'].iloc[0]
    max_spd = phase['velocity'].max()
    min_spd = phase['velocity'].min()
    max_vertrate_spd = phase['vertrate'].max()
    min_vertrate_spd = phase['vertrate'].min()
    del phase
    return [duration, avg_spd, std_spd,vertrate_avg_spd,vertrate_std_spd,delta_h,max_spd,min_spd,max_vertrate_spd,min_vertrate_spd]

def calculate_general_info(flight):
    start = int(flight[flight['phase']=='CL']['time'].iloc[0])
    end = int(flight[flight['phase']=='DE']['time'].iloc[-1])
    return start, end

## main

init_db()

path_to_dataset = "./test_flight_collection_with_phase/"

list_file_name = listdir(path_to_dataset)

aircraft = pd.read_csv('./aircraftDatabase.csv')

for file_name in list_file_name:
    print('filename:'+file_name)

    df = pd.read_csv(path_to_dataset+file_name)
    df.fillna(value={'phase':'NA'},inplace=True)
    
    descent = df[df['phase']=='DE']
    climb = df[df['phase']=='CL']
    cruise = df[df['phase']=='CR']

    if not(descent.empty) and not(climb.empty) and not(cruise.empty):
        db = get_db()

        desc_climb = calculate_descriptor(climb)
        db.execute("INSERT INTO climb (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,delta_h,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed) \
            VALUES (?,?,?,?,?,?,?,?,?,?)",
            desc_climb )

        desc_cruise = calculate_descriptor(cruise)
        desc_cruise.append(cruise['baroaltitude'].mean())
        desc_cruise.append(cruise['baroaltitude'].std())
        db.execute("INSERT INTO cruise (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,delta_h,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,mean_altitude,std_altitude) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            desc_cruise)



        desc_descent = calculate_descriptor(descent)
        db.execute("INSERT INTO descent (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,delta_h,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed) \
            VALUES (?,?,?,?,?,?,?,?,?,?)",
            desc_descent )
    
        start, end = calculate_general_info(df)
        icao=file_name.split('_')[1]
        airline = aircraft[aircraft['icao24']==icao].iloc[0]['operator']
        db.execute("INSERT INTO general_info (flight_start, flight_end, flight_duration,icao,airline) \
            VALUES (?,?,?,?,?)",(start,end, end-start, icao,airline))
        
        db.commit()
        db.close()


