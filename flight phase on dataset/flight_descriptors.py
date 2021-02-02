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
    #delta_h = phase['baroaltitude'].iloc[-1] - phase['baroaltitude'].iloc[0]
    max_spd = phase['velocity'].max()
    min_spd = phase['velocity'].min()
    max_vertrate_spd = phase['vertrate'].max()
    min_vertrate_spd = phase['vertrate'].min()
    del phase
    return [duration,avg_spd, std_spd,vertrate_avg_spd,vertrate_std_spd,max_spd,min_spd,max_vertrate_spd,min_vertrate_spd]


def calculate_metar(lat,lon,time):
    try:
        metar = pd.read_csv('../../data/metar/'+str(time)+'.csv', header=5,
                        usecols=['station_id','latitude','longitude','wind_speed_kt','temp_c','dewpoint_c','sea_level_pressure_mb'])

        metar = metar.merge(airports, left_on="station_id", right_on="ICAO", how='left', suffixes=('',''))
        metar['dist'] = (metar['latitude']-lat)**2+(metar['longitude']-lon)**2
        idmin = metar['dist'].idxmin(axis=1)
        weather = metar.loc[idmin]
        return [weather['Name'],weather['temp_c'],weather['dewpoint_c'],weather['wind_speed_kt']]

    except FileNotFoundError:
        return [None,np.NaN,np.NaN,np.NaN]

def calculate_general_info(flight):
    start = int(flight[flight['phase']=='CL']['time'].iloc[0])
    end = int(flight[flight['phase']=='DE']['time'].iloc[-1])
    return start, end

## main

init_db()

path_to_dataset = "../../data/flight_with_phase/"

list_file_name = listdir(path_to_dataset)

airline = pd.read_csv('../../data/airlines.csv')
airports=pd.read_csv('../../data/airports.csv',
                usecols=['Name','ICAO'])

for file_name in list_file_name:
    print('filename:'+file_name)

    df = pd.read_csv(path_to_dataset+file_name)
    
    descent = df[df['phase']=='DE']
    climb = df[df['phase']=='CL']
    cruise = df[df['phase']=='CR']

    db = get_db()
    
    if not(climb.empty):
        desc_climb = calculate_descriptor(climb)
        data_takeof = climb.iloc[0]
        lat = data_takeof['lat']
        lon = data_takeof['lon']
        time = (int(data_takeof['time'])//3600)*3600
        desc_climb += calculate_metar(lat,lon,time)
        db.execute("INSERT INTO climb (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,airport,temp_c,dewpoint_c,wind_spind_kt) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            desc_climb )
    else:
        db.execute("INSERT INTO climb DEFAULT VALUES")

    if not(cruise.empty):
        desc_cruise = calculate_descriptor(cruise)
        desc_cruise.append(cruise['baroaltitude'].mean())
        desc_cruise.append(cruise['baroaltitude'].std())
        db.execute("INSERT INTO cruise (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,mean_altitude,std_altitude) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            desc_cruise)
    else:
        db.execute('INSERT INTO cruise DEFAULT VALUES')


    if not(descent.empty):
        desc_descent = calculate_descriptor(descent)
        data_landing = descent.iloc[-1]
        lat = data_landing['lat']
        lon = data_landing['lon']
        time = (int(data_landing['time'])//3600)*3600
        desc_descent += calculate_metar(lat,lon,time)
        db.execute("INSERT INTO descent (duration, avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,airport,temp_c,dewpoint_c,wind_spind_kt) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            desc_descent )
    else:
        db.execute('INSERT INTO descent DEFAULT VALUES')

    #start, end = calculate_general_info(df)
    id_airline=file_name.split('_')[2][0:3]
    icao24 = file_name.split('_')[1]
    if len(airline[airline['ICAO']==id_airline])>0:
        airline_name = airline[airline['ICAO']==id_airline].iloc[0]['Airline']
    else:
        airline_name = None
        print(id_airline)
    db.execute("INSERT INTO general_info (icao,icao_airline,airline) \
        VALUES (?,?,?)",(icao24,id_airline,airline_name))

    db.commit()
    db.close()


