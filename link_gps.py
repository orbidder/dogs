# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:33:32 2018
Match Smooth accl to GPS data

From Supp Info:
9.	Using the link_gps.py script, merge the predicted classes of the accelerometer data (a product of the KNN)
 to the Latitude and Longitude values in the GPS data. Once the GPS data has behavioural classes, identify the 
 points where dogs are making left and right scent marks. These points then can be written to file for use in 
 GIS software or R for further analysis.

@author: Owen R. Bidder
"""
import pandas as pd
import numpy as np
import os
os.chdir('C:\\DataFolder\...') #Data location here

#Load in annotated accl data
smooth = pd.read_csv('dog_smooth_accl.csv') #smoothed predictions from smooth_knn.py
smooth.set_index('seconds', inplace=True)

#change seconds in to actual date and time
#Note for this dog, 445 seconds on accelerometer time is 2018-06-13 10:11:13.165

#Here's some code explaining my method
#this line will define a datetime that described actual time at 445 seconds
pd.to_datetime(pd.DataFrame({'year': [2018],'month': [6],'day': [13], 'hour':[10], 'minute':[11], 'second':[13.165]}))[0]

#make an array that describes the time difference (in datetime) using the index values in seconds
pd.to_timedelta(smooth.index, 's')
smooth.tail(10)
pd.to_timedelta(pd.Series(range(0,1841)), 's')


#define a datetime column by adding the timedelta to the origin
smooth['datetime'] = pd.to_datetime(pd.DataFrame({'year': [2018],'month': [6],'day': [13], 'hour':[10], 'minute':[11], 'second':[13]}))[0] + pd.to_timedelta(pd.Series(range(0,1842)), 's')

#now smooth['datetime'] will describe the actual time, which can be linked to the GPS timestamp

#Now do the same for the unobserved data
dog_unobs = pd.read_csv('dog_unobs_smooth_preds.csv') #smoothed predictions for the unobserved period, from smooth_knn.py
dog_unobs.set_index('seconds', inplace=True)
dog_unobs['datetime'] = pd.to_datetime(pd.DataFrame({'year': [2018],'month': [6],'day': [13], 'hour':[10], 'minute':[11], 'second':[13]}))[0] + pd.to_timedelta(dog_unobs.index, 's')

#a few lines here to check everything is as it should be
dog_unobs.columns
dog_unobs['Time']
dog_unobs['datetime']
#check that they match up
smooth.head(10)
smooth.tail(10)
dog_unobs.head(10) #looks good!

#Load in GPS data
fields = ['Date', ' Time', ' Latitude', ' Longitude'] #which columns to take from CSV file, many devices produce additional columns, NOTE: the IgotU device introduced a space before some column names i.e. " Time"
gps = pd.read_csv('Dog_GPS.csv', usecols=fields) #Your file name may differ, define it here
gps.columns = ['Date', 'Time', 'Latitude', 'Longitude'] #Remove those spaces from column names
gps.set_index(pd.to_datetime(gps.iloc[:,0] + ' ' + gps.iloc[:,1]), inplace=True)

#cut GPS data to observed validation period start/end
start = smooth.datetime.min()
end = smooth.datetime.max()
cut_gps = gps[(gps.index >= start) & (gps.index <= end)]

#merge labels to gps data
smooth_gps = smooth.merge(cut_gps, left_on=smooth.datetime, right_on=cut_gps.index, how='left')
smooth_gps.to_csv('dog_gps_labeled.csv') #a file that contains all KNN predictions and LAT/LON coordinates for the observed validation period

smooth_gps[smooth_gps['pred'] == 'scent'] #how many scents?

#Sometimes, the GPS may not be recording at the exact second the accelerometer predicts a scent mark. 
#The code below will find the nearest gps pos available and annotate, also recording the time difference to give an idea of location confidence/error 
#this function finds the nearest datetime in 'items' to the datetime 'pivot'
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

nearest(cut_gps.index, smooth[smooth['pred'] == 'scent'].iloc[0].datetime) #nearest was at 2018-05-11 14:59:47

#right = smooth_gps[(smooth_gps.key_0 == nearest(cut_gps.index, smooth[smooth['pred'] == 'right'].iloc[0].datetime))]
#left = smooth_gps[(smooth_gps.key_0 == nearest(cut_gps.index, smooth[smooth['pred'] == 'left'].iloc[0].datetime))]
scent = smooth_gps[(smooth_gps.key_0 == nearest(cut_gps.index, smooth[smooth['pred'] == 'scent'].iloc[0].datetime))]

#Annotate the GPS data with the unobserved predictions too
#Load in GPS data files
fields = ['Date', ' Time', ' Latitude', ' Longitude']
gps = pd.read_csv('Dog_GPS.csv', usecols=fields)
gps.columns
gps.columns = ['Date', 'Time', 'Latitude', 'Longitude']
gps['datetime'] = pd.to_datetime(gps.iloc[:,0] + ' ' + gps.iloc[:,1])
gps.set_index('datetime', inplace=True)

#cut GPS data to unobserved period
start = dog_unobs.datetime.min()
end = dog_unobs.datetime.max()
unobs_gps_only = gps[(gps.index >= start) & (gps.index <= end)]

#merge labels to gps data
unobs_gps = dog_unobs.merge(unobs_gps_only, left_on=dog_unobs.datetime, right_on=unobs_gps_only.index, how='left')
unobs_gps = unobs_gps.iloc[:,[1,2,5,6]]
unobs_gps.set_index('datetime', inplace=True)

unobs_gps[(unobs_gps['pred'] == 'scent')] #how many scent-marks?
unobs_gps['dt'] = unobs_gps.index
#not all scent marks had gps during event, so let's find nearest

for i in range(len(scent_marks)):
    nrest = nearest(unobs_gps_only.index, unobs_gps[(unobs_gps['pred'] == 'scent')].dt.iloc[i])
    scent_marks.iloc[i,4] = pd.to_timedelta(scent_marks.iloc[i].name-nrest, 's').total_seconds()
    scent_marks.iloc[i,1] = unobs_gps.Latitude[(unobs_gps.index == nrest)].values
    scent_marks.iloc[i,2] = unobs_gps.Longitude[(unobs_gps.index == nrest)].values

scent_marks.to_csv('Dog_unobs_scentmarks.csv') #This file describes all of the scent-mark times and locations from the unobserved (deployment) period

#This code in case you need all behavioural types
#unobs_gps = unobs_gps[unobs_gps.Latitude.notnull()]
#unobs_gps.to_csv('gps_unobs_labelled.csv')

#Personally, I prefer the mapping tools available in R and QGIS.
#If you would prefer to map these locations in Python, here is some simple code that you can extend for your purposes

#plot left and right scent marks on a map
from gmplot import gmplot
smooth_gps.columns

#center map
gmap = gmplot.GoogleMapPlotter(scent_marks['Latitude'].mean(), scent_marks['Longitude'].mean(), 13) #lat, log, zoom
gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
#take left and right scent mark coords and plot
points = scent_marks
gmap.scatter(points.Latitude.values, points.Longitude.values, color='#3B0B39', size=20)
gmap.draw('scentmarks.html')

#make a map of all locations
gps_all = smooth_gps[np.isfinite(smooth_gps.Latitude)]

gmap = gmplot.GoogleMapPlotter(smooth_gps['Latitude'].mean(), smooth_gps['Longitude'].mean(), 13) #lat, log, zoom
gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
#take left and right scent mark coords and plot
gmap.heatmap(gps_all.Latitude.values, gps_all.Longitude.values) #makes a heatmap of point locations
gmap.scatter(points.Latitude.values, points.Longitude.values, color='#3B0B39', size=2, marker = False)
gmap.draw('allpoints.html')
