#!/usr/bin/env python
# coding: utf-8

# In[79]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from openap import FlightPhase
from os import listdir
import os

# In[80]:


m_to_ft = 3.28084
m_by_s_to_ft_by_min = 3.28084*60
m_by_s_to_kt = 1.94384


# In[81]:

path_to_dataset = "./test_flight_collection/"
result_dir = "./test_flight_collection_with_phase/"
os.mkdir(result_dir)

list_file_name = listdir(path_to_dataset)

for file_name in list_file_name:
    df = pd.read_csv(path_to_dataset+file_name)
    df['time']= df['time'] - df['time'][0]

    phase_slicer = FlightPhase()
    phase_slicer.set_trajectory(df['time'],df['baroaltitude'].values*m_to_ft,df['velocity'].values*m_by_s_to_kt, df['vertrate'].values*m_by_s_to_ft_by_min)

    df['phase'] = phase_slicer.phaselabel()


    with open(result_dir + 'phase_'+file_name,'w') as file:
        file.write(df.to_csv(index=False))

