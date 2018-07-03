# -*- coding: utf-8 -*-
"""
Loading in large CSV and cropping them
Created on Tue Jun 26 09:36:14 2018

@author: Owen
"""
import pandas as pd
import os
chunksize = 30*10**6

os.chdir('C:\\Data\Hopland Dogs\GPS Data Nate')
filename = '32946_0000000004.resampled.csv'
for chunk in pd.read_csv(filename, chunksize=chunksize):
    process(chunk)
    
#Convert time column to datetime format    
chunk['Time'] = pd.to_datetime(chunk['Time'])

##Look at last time in chunk
chunk.tail(1)
chunk.tail(1)[3]


#plot x-axis to see if whole deployment is present
time = chunk.iloc[:,0]
x = chunk.iloc[:,1]
y = chunk.iloc[:,2]
z = chunk.iloc[:,3]

chunk['Accel-Y (g)']
#plot just last 100 rows to see if the device is still attached
import matplotlib.pyplot as plt

plt.plot(time.head(10000000), y.head(10000000), color='lightblue', linewidth=3)

plt.show()

#shows we have the right file size
#now write to csv
chunk.to_csv('Nate_ACCL.csv')

new = chunk.head(10000000)
new.to_csv('first_mil.csv')