# -*- coding: utf-8 -*-
"""
Loading in large CSV and cropping them
Created on Tue Jun 26 09:36:14 2018

From Supp Inf
2.	Do a quick summary plot using the crop_spyder.py. 
We used this script to crop the file, as the device continued to record after it was removed from the dogs, 
producing large files with superfluous data. Use the ‘chunksize’ argument to specify how many rows should 
be taken from the start of the file.

@author: Owen R Bidder
"""
import pandas as pd
import os
chunksize = 10*10**4 #change here to set number of rows to load from start of file

os.chdir('C:\\DataFolder\...')
filename = '' #file name in folder here

chunk = pd.read_csv(filename, nrows =chunksize)

#Convert time column to datetime format    
chunk['Time'] = pd.to_datetime(chunk['Time'])

##Look at last time in chunk
chunk.tail(1)[3]


#plot axes to see if whole deployment is present
time = chunk.iloc[:,0]
x = chunk.iloc[:,1]
y = chunk.iloc[:,2]
z = chunk.iloc[:,3]

#plot just last 100 rows to see if the device is still attached
import matplotlib.pyplot as plt
plt.plot(time.tail(100), y.tail(100), color='lightblue', linewidth=3)
plt.show()

#shows we have the right file size
#now write to csv
chunk.to_csv('') # pick a filename for output