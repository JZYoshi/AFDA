#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from openap import FlightPhase
from os import listdir
import os

## rules to clean the data

def is_complete(df,t_nb_points_high=100,t_altitude=5000,t_min_altitude=500, nb_point_desc=100, nb_point_cl=100):
    min_cl = df['baroaltitude'].iloc[0:nb_point_cl].min()
    min_desc = df['baroaltitude'].iloc[len(df)-nb_point_desc:].min()
    nb_point_high = len(df[df['baroaltitude']>t_altitude])

    return min_cl<t_min_altitude and min_desc<t_min_altitude and nb_point_high>t_nb_points_high


def enough_data(df,time_threshold=10*60,altitude_min=500):
    df['diff']=df['time'].diff()
    index = df[(df['diff']>time_threshold) & (df['baroaltitude']>altitude_min)].index
    return len(index)==0


def remove_jump(df,t1=1000,t2=100):
    index = df.index
    i=0
    index = []
    h = df['baroaltitude']
    while i<len(h)-1:
        diff = np.abs(h[i]-h[i+1])
        if diff>t1:
            index.append(i+1)
            i+=1
            while i<len(h)-1 and np.abs(h[i]-h[i+1])<t2:
                index.append(i+1)
                i+=1
        i+=1
        
    df.drop(index=index,inplace=True)
    df.reset_index(inplace=True)


## program
m_to_ft = 3.28084
m_by_s_to_ft_by_min = 3.28084*60
m_by_s_to_kt = 1.94384




path_to_dataset = "./test_flight_collection/"
result_dir = "./test_flight_collection_with_phase/"
os.mkdir(result_dir)

list_file_name = listdir(path_to_dataset)

for file_name in list_file_name:
    print('filename:'+file_name)
    df = pd.read_csv(path_to_dataset+file_name)
    
    df.dropna(subset=['baroaltitude',], inplace=True)
    df.reset_index(inplace=True)

    if enough_data(df) and is_complete(df):
        remove_jump(df)

        df['time']= df['time'] - df['time'][0]

        phase_slicer = FlightPhase()
        phase_slicer.set_trajectory(df['time'],df['baroaltitude'].values*m_to_ft,df['velocity'].values*m_by_s_to_kt, df['vertrate'].values*m_by_s_to_ft_by_min)

        df['phase'] = phase_slicer.phaselabel()


        with open(result_dir + 'phase_'+file_name,'w') as file:
            file.write(df.to_csv(index=False))

