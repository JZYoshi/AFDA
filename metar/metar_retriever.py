import requests
import pandas as  pd
import numpy as np
import time

def retrieve_metar():
    url = 'https://www.aviationweather.gov/adds/dataserver_current/current/metars.cache.csv'
    r = requests.get(url)
    with open('../../data/metar/'+str((int(time.time())//3600) *3600)+'.csv','wb') as metar:
        metar.write(r.content)


## main program
last_time=time.time()
while True:
    if time.time()-last_time>=3600:
        retrieve_metar()
        last_time=time.time()
        