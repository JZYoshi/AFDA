from opensky_api import OpenSkyApi
import time
import os
import pandas as pd

def periodic_retrieve(period, handler, in_parallel):

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


def distribute_to_indiv_files(states, tempo_dname='./__tempo', format='.csv'):
    if states is not None:
        global aircraft_database
        try:
            aircraft_database
        except:
            aircraft_database = pd.read_csv('../dataset/aircraftDatabase.csv', low_memory=False)
        
        if not os.path.exists(tempo_dname):
            os.mkdir(tempo_dname)
        t = states.time
        for state in states.states:
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


def match_conditions(id_dict, conditions, aircraft_database):
    q = '&'.join([ '(' + k + '==' + f'"{str(v)}"' + ')' for (k,v) in id_dict.items() ])
    entry = aircraft_database.query(q)
    if entry.empty:
        return False
    else:
        for (k, v) in conditions.items():
            if not all(entry[k].str.match(v, na=False)):
                return False
    return True


def print_states(s):
    if s is not None:
        print(f'At {s.time}, get {len(s.states)} states')
    else:
        print('failed to get data')

# aircraft_database = pd.read_csv('../dataset/aircraftDatabase.csv', low_memory=False)
# periodic_retrieve(10, distribute_to_indiv_files, True)
periodic_retrieve(10, print_states, True)
