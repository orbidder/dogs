# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 15:43:31 2018
From Supp Inf
4.	We must synchronize the timestamp of the accelerometer data with the video 
that details to behavioural observations of the dog. At the beginning of the 
observation period, we performed conspicuous calibration tilts (the device was 
rotated 90 degrees for 5 second, and this was repeated 3 times). With this in mind, 
use subsample.py to plot 10-minute summaries of the data. The function will run through 
the first 3 days of the file (after that the tag was off the animal and so it's just 
excess data), showing a 10 minute window in each plot to help you find the calibration 
tilts mentioned previously. This function needs there to be a folder called 'explore', 
which will be filled with plots for you to run through sequentially (using Windows’ Photo 
app for instance). In future, we will implement a more elegant interactive plot for Users 
to use in Python, but this is currently in development. Once the tilts are identified and 
their time in the accelerometer file noted, you can trim the start of the file to ca. 5 seconds 
before the tilts, to make them easy to spot and sync to the video in ELAN.
@author: Owen R. Bidder
"""

import pandas as pd
import os

os.chdir('C:\\DataFolder\...') #Data location here
filename = '' #filename from crop_file.py
dog_df = pd.read_csv(filename, usecols = ['Time', 'Accel-X (g)', ' Accel-Y (g)', ' Accel-Z (g)']) #Use only specific columns, this arguement can be changed based on format produced by device
dog_df.set_index('Time', inplace=True) #set the index to time column

twentyHz = dog_df.iloc[1::2,:] #take every 2nd row to downsample (halves the sample rate)

twentyHz.to_csv('dog_dfmine_Twenty.csv') #save a copy of downsampled data

##Plot in matplotlib the first 1000 rows
import matplotlib.pyplot as plt
plt.plot(twentyHz.head(1000), color='lightblue', linewidth=3) 
plt.show()

#####################################################
#Search for calibration tilts
# code needs an output folder, called 'explore'
path = 'C:\\DataFolder\explore'
try:  
    os.mkdir(path)
except OSError:  
    print ("Creation of the directory %s failed" % path)
else:  
    print ("Successfully created the directory %s " % path)
	
#Here we can use the datetime record in our accl data, and the time the device was started, to produce an 'elapsed seconds' column
twentyHz['seconds'] = (pd.to_datetime(twentyHz.index) - pd.to_datetime(pd.DataFrame({'year': [2018],'month': [6],'day': [13], 'hour':[9], 'minute':[36], 'second':[27.525]}))[0]).total_seconds()
twentyHz.set_index(twentyHz['seconds'], inplace=True) #change the index to seconds elapsed
twentyHz['minutes'] = twentyHz['seconds']/60
twentyHz.set_index(twentyHz['minutes'], inplace=True)

#For this example, I made plots for a range of 0 to 1440 (1440 minutes is 24 hours)
#With that, I found the tilts between 132 and 134 minutes in to the file
#Your data may differ

for counter in range(0,1440):
    start = counter*1
    stop = start + 10
    fig = twentyHz[(twentyHz['minutes'] > start) & (twentyHz['minutes'] < stop)].iloc[:,0:3].plot(figsize=(20,10)).get_figure()
    dir_name = 'C:\\Data\Hopland Dogs\dog_dfmine\explore'
    base_filename = '{0}{1}'.format('output',counter)
    suffix = '.jpg'
    fig.savefig(os.path.join(dir_name, base_filename + suffix))
    plt.close(fig)
    #input("Press Enter to continue...")

#Load back in the dog_df 20Hz data
twentyHz = pd.read_csv('dog_df_Twenty.csv')
twentyHz.set_index('Time', inplace=True)
twentyHz['seconds'] = (pd.to_datetime(twentyHz.index) - pd.to_datetime(pd.DataFrame({'year': [2018],'month': [6],'day': [13], 'hour':[9], 'minute':[36], 'second':[27.525]}))[0]).total_seconds()
twentyHz['minutes'] = twentyHz['seconds']/60
   
#To write this one, I used the 'minutes' column, the tilts start ~27 minutes in to the data   
start = 27
stop = start + 2
twentyHz[(twentyHz['minutes'] > start) & (twentyHz['minutes'] < stop)].iloc[:,0:3].plot(figsize=(20,10)) #are tilts visible? 

cut = twentyHz[(twentyHz['minutes'] > 27)] #cut the file to just before the calibration tilts
cut.head(1000).iloc[:,0:3].plot() #check with a quick plot

#set seconds to start from 0
cut.iloc[0,]
cut['seconds'] = cut['seconds']-1620.040000
cut['minutes'] = cut['minutes']-27.000667
cut.iloc[0:1000,0:3].plot(figsize=(20,10))

cut.to_csv('dog_df_Cut.csv') #write to file, for loading in to ELAN
print('Finished writing')
