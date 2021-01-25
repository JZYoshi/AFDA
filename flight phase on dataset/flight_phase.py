#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from openap import FlightPhase
from os import listdir
import os
import warnings
warnings.filterwarnings('ignore')

## rules to clean the data
def split_flights(df):
    diff = df['time'].diff()>=3600
    index = diff[diff==True].index
    
    flights = []
    first=0
    for i in index:
        flights.append(df.iloc[first:i].reset_index())
        first = i
    flights.append(df.iloc[first:])
    return flights


def enough_data(df):
    min_data = 40 #(une montee avec 2 points par minutes)
    df = df.copy()
    df.dropna(subset=['baroaltitude'], inplace=True)
    if len(df)<=min_data:
        return False
    return True

def check_and_drop_phase(df):
    # calcul nombre de points par phase
    nb_point_cl = len(df[df['phase']=='CL'])
    nb_point_cr = len(df[df['phase']=='CR'])
    nb_point_de = len(df[df['phase']=='DE'])
    
    # calcul présence de phase
    de = (len(df[df['phase']=='DE'])>=10)
    cr = (len(df[df['phase']=='CR'])>=10)
    cl = (len(df[df['phase']=='CL'])>=10)
    
    # calcul des trous max par phase
    hole_cl = df[df['phase']=='CL']['time'].diff().max()
    hole_cr = df[df['phase']=='CR']['time'].diff().max()
    hole_de = df[df['phase']=='DE']['time'].diff().max()
    
    #phase climb
    if cl:
        is_begin_cl = (df['baroaltitude'].iloc[0:10].min() <= 2000)
        if (hole_cl>=240) or not(is_begin_cl) or not(cr):
            df.drop(labels=df[df['phase']=='CL'].index, inplace=True)
    else:
        df.drop(labels=df[df['phase']=='CL'].index, inplace=True)
    
    # phase croisiere
    if (hole_cr>=1080) or not(cl) or not(de) or not(cr):
        df.drop(labels=df[df['phase']=='CR'].index, inplace=True)

    #phase descent
    if de:
        is_end_de = (df['baroaltitude'].iloc[len(df)-10:].min() <= 2000)
        if (hole_de>=240) or not(is_end_de) or not(cr):
            df.drop(labels=df[df['phase']=='DE'].index, inplace=True)
    else:
        df.drop(labels=df[df['phase']=='DE'].index, inplace=True)
        
    return df[(df['phase']=='CL') | (df['phase']=='CR') | (df['phase']=='DE')]


## program
m_to_ft = 3.28084
m_by_s_to_ft_by_min = 3.28084*60
m_by_s_to_kt = 1.94384




path_to_dataset = "../../__tempo/"
result_dir = "../../flight_with_phase/"
os.mkdir(result_dir)

list_file_name = listdir(path_to_dataset)

i=0
nb_files = len(list_file_name)

for file_name in list_file_name:
    i+=1
    print('filename:'+file_name)
    print('file '+str(i)+' over '+str(nb_files))
    df = pd.read_csv(path_to_dataset+file_name, na_values='None')
    
    df.dropna(subset=['baroaltitude',], inplace=True)
    df.reset_index(inplace=True)
    list_flight = split_flights(df)
    j=0
    for flight in list_flight:
        j+=1
        if enough_data(flight):
            
            flight['time_bis']= flight['time'] - flight['time'].iloc[0]
            phase_slicer = FlightPhase()
            phase_slicer.set_trajectory(flight['time_bis'].values,flight['baroaltitude'].values*m_to_ft,flight['velocity'].values*m_by_s_to_kt, flight['vertrate'].values*m_by_s_to_ft_by_min)

            flight['phase'] = phase_slicer.phaselabel()
            flight.drop(columns='time_bis', inplace=True)

            flight = check_and_drop_phase(flight)
            if len(flight)>0:
                with open(result_dir + 'phase_'+file_name+'_'+str(j),'w') as file:
                    file.write(flight.to_csv(index=False))

