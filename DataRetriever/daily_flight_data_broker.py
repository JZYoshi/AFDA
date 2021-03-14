from opensky_api import OpenSkyApi
import time
import os
import pandas as pd

def periodic_retrieve(period, handler, in_parallel):
    """
    To call the OpenSky Network API every *period*, and process the data with the *handler*.
    The retrieval and the processing can be executed in parallel.

    :param period: period in second (int)

    :param handler: a function that takes result of API call as parameter

    :param in_parallel: a boolean indicating whether the retrieval and the processing are executed in parallel 
    """
    api = OpenSkyApi()

    if in_parallel == True:
        from queue import SimpleQueue
        global states_queue
        states_queue = SimpleQueue()
        
        def worker():
            while True:
                entry = states_queue.get(block=True, timeout=None)
                handler(entry)
        
        import threading
        threading.Thread(target=worker, daemon=True).start()

    next_call = time.time()
    while True:
        print(f"now is {time.time()}")
        data = api.get_states()
        if in_parallel == False:
            handler(data)
        else:
            states_queue.put(data)
        next_call = next_call + period
        time.sleep(max(next_call - time.time(), 0))


def distribute_to_indiv_files(API_res, tempo_dname='../data/__tempo'):
    """
    To explore the state vectors in the response of the API call, 
    and distribute useful data into files according to their flight numbers.
    The files' names will be the combination of icao24 and callsign.

    :param API_res: result of an OpenSky Network API call
    """
    format='.csv'
    if API_res is not None:
        global aircraft_database
        try:
            aircraft_database
        except:
            aircraft_database = pd.read_csv('../data/aircraftDatabase.csv', low_memory=False)
        
        if not os.path.exists(tempo_dname):
            os.mkdir(tempo_dname)
        t = API_res.time
        for state in API_res.states:
            id_dict = { 'icao24': state.icao24.strip() }
            conditions = {'manufacturericao': 'AIRBUS', 'typecode': r'\bA318\b|\bA319\b|\bA320\b|\bA321\b'}
            if not match_conditions(id_dict, conditions, aircraft_database):
                continue
            print(f'Got one! {state.icao24}, {state.callsign}')
            fname = state.icao24.strip() + '_' + state.callsign.strip()
            if not os.path.exists(tempo_dname + '/' + fname + format):
                f = open(tempo_dname + '/' + fname + format, 'a+')
                f.write('time,lat,lon,velocity,heading,vertrate,onground,spi,squawk,baroaltitude,geoaltitude,lastposupdate,lastcontact \n')
            else:
                f = open(tempo_dname + '/' + fname + format, 'a+')
            f.write(','.join(map(str, [t, state.latitude, state.longitude, state.velocity, state.heading, state.vertical_rate, state.on_ground, 
                state.spi, state.squawk, state.baro_altitude, state.geo_altitude, state.time_position, state.last_contact])) + '\n')
            f.close()


def match_conditions(id_dict, conditions, aircraft_database_df):
    """
    To tell whether an aircraft with its identification described by *id_dict* satisfies the given *conditions*
    that are related to the aircraft. *aircraft_database_df* should be a dataframe of the aircraft database given
    by the OpenSky Network <https://opensky-network.org/datasets/metadata/>_, and it contains all the info of aircrafts. 

    :param id_dict: a dict describing the identification of an aircraft (key: a label of aircraft_database)

    :param conditions: a dict describing the conditions that an aircraft should meet (key: a label of aircraft_database)

    :param aircraft_database_df: a dataframe of aircraft database provided by OpenSky Network <https://opensky-network.org/datasets/metadata/>_    
    """
    q = '&'.join([ '(' + k + '==' + f'"{str(v)}"' + ')' for (k,v) in id_dict.items() ])
    entry = aircraft_database_df.query(q)
    if entry.empty:
        return False
    else:
        for (k, v) in conditions.items():
            if not all(entry[k].str.match(v, na=False)):
                return False
    return True


def print_states(s):
    """
    To print the info of a response of the OpenSky Network API call, 
    including the time and its states vectors length.
    """
    if s is not None:
        print(f'At {s.time}, get {len(s.states)} states')
    else:
        print('failed to get data')

if __name__=="__main__":
    aircraft_database = pd.read_csv('../data/aircraftDatabase.csv', low_memory=False)
    periodic_retrieve(10, distribute_to_indiv_files, True)
