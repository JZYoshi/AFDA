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
import time as clock
from mpi4py import MPI
import itertools

## functions
def calculate_descriptor(phase):
    """
    Compute the descriptors for a specific flight phase.
    The computed descriptors are:

        + duration
        + average speed
        + standard deviation of speed
        + average vertical speed
        + standard deviation of vertical speed
        + max speed
        + min speed
        + max vertical speed
        + min vertical speed

    :param phase: a dataframe containing only the flight phase to analyse
    :returns: the list of descriptors as explained above
    """
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
    """
    Determine the closest airport from a point and find
    the weather condition at this airport and at the input time

    :param lat: the lattitude
    :param lon: the longitude
    :param time: the time
    :returns: a list containing airport name, temperature(in Celcius), dewpoint(in Celcius) and wind speed(in kt) 
    """
    try:
        metar = pd.read_csv('../data/metar/'+str(time)+'.csv', header=5,
                        usecols=['station_id','latitude','longitude','wind_speed_kt','temp_c','dewpoint_c','sea_level_pressure_mb'])

        metar = metar.merge(airports, left_on="station_id", right_on="ICAO", how='left', suffixes=('',''))
        metar['dist'] = (metar['latitude']-lat)**2+(metar['longitude']-lon)**2
        idmin = metar['dist'].idxmin(axis=1)
        weather = metar.loc[idmin]
        return [weather['Name'],weather['temp_c'],weather['dewpoint_c'],weather['wind_speed_kt']]

    except (FileNotFoundError, KeyError) as e:
        return [None,np.NaN,np.NaN,np.NaN]

# compute descriptors and save them in database for each flight phase 
def compute_descriptors_wrap_function(file_name, sql_query_queue):
    df = pd.read_csv(path_to_dataset+file_name)

    descent = df[df['phase']=='DE']
    climb = df[df['phase']=='CL']
    cruise = df[df['phase']=='CR']

    # compute descriptors for climb phase
    if not(climb.empty):
        desc_climb = calculate_descriptor(climb)
        data_takeof = climb.iloc[0]
        lat = data_takeof['lat']
        lon = data_takeof['lon']
        time = (int(data_takeof['time'])//3600)*3600
        desc_climb += calculate_metar(lat,lon,time)
        sql_query_queue.put(["INSERT INTO climb (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,airport,temp_c,dewpoint_c,wind_speed_kt) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            desc_climb])
    else:
        sql_query_queue.put(["INSERT INTO climb DEFAULT VALUES"])

    #compute descriptors for cruise phase
    if not(cruise.empty):
        desc_cruise = calculate_descriptor(cruise)
        desc_cruise.append(cruise['baroaltitude'].mean())
        desc_cruise.append(cruise['baroaltitude'].std())
        sql_query_queue.put(["INSERT INTO cruise (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,mean_altitude,std_altitude) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            desc_cruise])
    else:
        sql_query_queue.put(['INSERT INTO cruise DEFAULT VALUES'])

    # compute descriptors for descent phase
    if not(descent.empty):
        desc_descent = calculate_descriptor(descent)
        data_landing = descent.iloc[-1]
        lat = data_landing['lat']
        lon = data_landing['lon']
        time = (int(data_landing['time'])//3600)*3600
        desc_descent += calculate_metar(lat,lon,time)
        sql_query_queue.put(["INSERT INTO descent (duration, avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,airport,temp_c,dewpoint_c,wind_speed_kt) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            desc_descent])
    else:
        sql_query_queue.put(['INSERT INTO descent DEFAULT VALUES'])

    # get airline corresponding to the flight
    id_airline=file_name.split('_')[2][0:3]
    icao24 = file_name.split('_')[1]
    if len(airline[airline['ICAO']==id_airline])>0:
        airline_name = airline[airline['ICAO']==id_airline].iloc[0]['Airline']
    else:
        airline_name = None
        unknown_airline.append(id_airline)
    sql_query_queue.put(["INSERT INTO general_info (icao,icao_airline,airline) \
        VALUES (?,?,?)",(icao24,id_airline,airline_name)])


def sql_query_executor(sql_query_queue, time):
    db_connection = get_db()
    while True:
        try:
            time["end"] = clock.time()
            query = sql_query_queue.get(block=True, timeout=5)
        except queue.Empty:
            print("no more queries to execute")
            db_connection.commit()
            db_connection.close()
            break
        else:
            if len(query) == 1:
                db_connection.execute(query[0])
            else:
                db_connection.execute(query[0], query[1])
            
    

## main
if __name__=="__main__":
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    path_to_dataset = "../data/flight_with_phase/"

    if rank == 0:
        # initialisation ( initialiase database, useful dataframe, print info)
        init_db()

        l = listdir(path_to_dataset)
        list_file_name = [l[i:i+len(l)//size] for i in range(0,len(l)-len(l)%size,len(l)//size)]
        list_file_name[0]+=l[len(l)-len(l)%size:]

        N = len(l)
        print('number of file to be processed:', N)
        start = clock.time()
    else:
        list_file_name =None

    list_file_name = comm.scatter(list_file_name, root=0)

    query_list = []

    airline = pd.read_csv('../data/airlines.csv')
    airports=pd.read_csv('../data/airports.csv',
                    usecols=['Name','ICAO'])



    i=0
    unknown_airline=[]

    # loop which compute descriptors and save them in database for each flight phase  
    for file_name in list_file_name:

        df = pd.read_csv(path_to_dataset+file_name)

        descent = df[df['phase']=='DE']
        climb = df[df['phase']=='CL']
        cruise = df[df['phase']=='CR']

        # compute descriptors for climb phase
        if not(climb.empty):
            desc_climb = calculate_descriptor(climb)
            data_takeof = climb.iloc[0]
            lat = data_takeof['lat']
            lon = data_takeof['lon']
            time = (int(data_takeof['time'])//3600)*3600
            desc_climb += calculate_metar(lat,lon,time)
            query_list.append("INSERT INTO climb (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,airport,temp_c,dewpoint_c,wind_spind_kt) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s,%s)"%tuple(desc_climb))
        else:
            query_list.append("INSERT INTO climb DEFAULT VALUES")

        #compute descriptors for cruise phase
        if not(cruise.empty):
            desc_cruise = calculate_descriptor(cruise)
            desc_cruise.append(cruise['baroaltitude'].mean())
            desc_cruise.append(cruise['baroaltitude'].std())
            query_list.append("INSERT INTO cruise (duration,avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,mean_altitude,std_altitude) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%tuple(desc_cruise))
        else:
            query_list.append('INSERT INTO cruise DEFAULT VALUES')

        # compute descriptors for descent phase
        if not(descent.empty):
            desc_descent = calculate_descriptor(descent)
            data_landing = descent.iloc[-1]
            lat = data_landing['lat']
            lon = data_landing['lon']
            time = (int(data_landing['time'])//3600)*3600
            desc_descent += calculate_metar(lat,lon,time)
            query_list.append("INSERT INTO descent (duration, avg_speed,std_speed,avg_vertrate_speed,std_vertrate_speed,max_spd,min_spd,max_vertrate_speed,min_vertrate_speed,airport,temp_c,dewpoint_c,wind_spind_kt) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s,%s)"%tuple(desc_descent))
                
        else:
            query_list.append('INSERT INTO descent DEFAULT VALUES')

        # get airline corresponding to the flight
        id_airline=file_name.split('_')[2][0:3]
        icao24 = file_name.split('_')[1]
        if len(airline[airline['ICAO']==id_airline])>0:
            airline_name = airline[airline['ICAO']==id_airline].iloc[0]['Airline']
        else:
            airline_name = None
            unknown_airline.append(id_airline)
        query_list.append("INSERT INTO general_info (icao,icao_airline,airline) \
            VALUES ('%s','%s','%s')"%(icao24,id_airline,airline_name))

    query_list = comm.gather(query_list, root=0)

    if rank == 0:
    	query_list = list(itertools.chain(*query_list))
    	db = get_db()
    	for query in query_list:
    		query = query.replace('None','NULL')
    		query = query.replace('nan','NULL')
    		query = query.replace("'NULL'",'NULL')
    		db.execute(query)

    	db.commit()
    	db.close()

    	total_time = clock.time() - start
    	print("process end with success")
    	print('total_time:', total_time)
    	print('process time by file:', total_time/N)
