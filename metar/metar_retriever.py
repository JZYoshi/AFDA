import requests
import pandas as  pd
import numpy as np
import time
import os

def retrieve_metar():
    """
    This function downloads a file containing metar data.
    The url of the downloaded data is `metar_data <https://www.aviationweather.gov/adds/dataserver_current/current/metars.cache.csv>`_
    Finally the name of the file which is created corresponds to the unix time of the hour of the downloading.
    """
    url = 'https://www.aviationweather.gov/adds/dataserver_current/current/metars.cache.csv'
    r = requests.get(url)
    if not os.path.exists('../data/metar'):
            os.mkdir('../data/metar')
    with open('../data/metar/'+str((int(time.time())//3600) *3600)+'.csv','wb') as metar:
        metar.write(r.content)
        print("succefuly download "+str((int(time.time())//3600) *3600)+'.csv')


## main program
if __name__=="__main__":
    retrieve_metar()
