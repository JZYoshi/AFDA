import pandas as pd
import numpy as np

def init_column(df):
    df['departure']=None
    df['arrival']=None
    df['temp_c_start']=None
    df['temp_c_end']=None
    df['dewpoint_c_start']=None
    df['dewpoint_c_end']=None
    df['wind_speed_kt_start']=None
    df['wind_speed_kt_end']=None

def which_phase(flight):
    return np.isnan(flight['duration_climb']),
           np.isnan(flight['duration_descent'])

def calculate_descriptors(df):
    n = len(df)
    airports=pd.read_csv('../../data/airports.csv',
                    usecols=['Name','ICAO'])
    for i in range(n):
        flight = df.iloc[i]
        climb, descent = which_phase(flight)
        
        if climb:
            # calcul of weather
            lat = flight['lat_start']
            lon = flight['long_start']
            end_time = (int(flight['start_time'])//3600)*3600
            metar = pd.read_csv(metar_path+str(end_time)+'.csv', header=5,
                                usecols=['station_id','latitude','longitude','wind_speed_kt','temp_c','dewpoint_c','sea_level_pressure_mb'])
            metar = metar.merge(airports, left_on="station_id", right_on="ICAO", how='left', suffixes=('',''))
            metar['dist'] = (metar['latitude']-lat)**2+(metar['longitude']-lon)**2
            idmin = metar['dist'].idxmin(axis=1)
            weather = metar.loc[idmin]

            #assigner les valeurs de weather avec at ou iat
            df.at[i,'departure'] = weather['Name']
            df.at[i,'temp_c_end'] = weather['temp_c']
            df.at[i,'dewpoint_c_end'] = weather['dewpoint_c']
            df.at[i,'wind_speed_kt_end'] = weather['wind_speed_kt']

        if descent:
            # calcul of weather
            lat = flight['lat_end']
            lon = flight['long_end']
            end_time = (int(flight['end_time'])//3600)*3600
            metar = pd.read_csv(metar_path+str(end_time)+'.csv', header=5,
                                usecols=['station_id','latitude','longitude','wind_speed_kt','temp_c','dewpoint_c','sea_level_pressure_mb'])
            metar = metar.merge(airports, left_on="station_id", right_on="ICAO", how='left', suffixes=('',''))
            metar['dist'] = (metar['latitude']-lat)**2+(metar['longitude']-lon)**2
            idmin = metar['dist'].idxmin(axis=1)
            weather = metar.loc[idmin]

            #assigner les valeurs de weather avec at ou iat
            df.at[i,'arrival'] = weather['Name']
            df.at[i,'temp_c_end'] = weather['temp_c']
            df.at[i,'dewpoint_c_end'] = weather['dewpoint_c']
            df.at[i,'wind_speed_kt_end'] = weather['wind_speed_kt']
    




## main program

# read descriptors
filepath = '../../data/'
filename = 'descriptors.csv'
df = pd.read_csv(filepath+filename)

## init new columns

