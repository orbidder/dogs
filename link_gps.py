# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:33:32 2018
Match Smooth accl to GPS data
@author: Owen R. Bidder
"""
import pandas as pd
import numpy as np
import os
os.chdir('C:\\Data\Hopland Dogs\GPS Data Nate')

#Load in annotated accl data
smooth = pd.read_csv('smooth_accl.csv')
smooth.set_index('seconds', inplace=True)

#change seconds in to actual date and time
#Note 24 seconds on ACCL time is 11/05/2018 14:32:00
#So 0 seconds on ACCL is 11/05/2018 14:31:36
#So 539 seconds on ACCL is 11/05/2018 14:40:34
#Here's some code explaining my method

#set a datetime that described actual time 
pd.to_datetime(pd.DataFrame({'year': [2018],'month': [5],'day': [11], 'hour':[14], 'minute':[31], 'second':[00]}))[0]

#make an array that describes the time difference (in datetime) using the index values in seconds
pd.to_timedelta(smooth.index, 's')

#define a datetime column by adding the timedelta to the origin
smooth['datetime'] = pd.to_datetime(pd.DataFrame({'year': [2018],'month': [5],'day': [11], 'hour':[14], 'minute':[31], 'second':[00]}))[0] + pd.to_timedelta(smooth.index, 's')
#Boom

#Load in GPS data
fields = ['Date', 'Time', 'Latitude', 'Longitude']
gps = pd.read_csv('Nate_051118_051518_dog.csv', usecols=fields)
gps.columns
gps.set_index(pd.to_datetime(gps.iloc[:,0] + ' ' + gps.iloc[:,1]), inplace=True)

#cut GPS data to observed period
start = smooth.datetime.min()
end = smooth.datetime.max()
cut_gps = gps[(gps.index >= start) & (gps.index <= end)]

#merge labels to gps data
smooth_gps = smooth.merge(cut_gps, left_on=smooth.datetime, right_on=cut_gps.index, how='left')
smooth_gps.to_csv('gps_labeled.csv')

#for some reason gps wasn't recording at the moment dog peed right, so let's find the nearest gps pos available 
#this function finds the nearest datetime in 'items' to the datetime 'pivot'
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

nearest(cut_gps.index, smooth[smooth['pred'] == 'right'].iloc[0].datetime) #nearest was at 2018-05-11 14:59:47

right = smooth_gps[(smooth_gps.key_0 == nearest(cut_gps.index, smooth[smooth['pred'] == 'right'].iloc[0].datetime))]
left = smooth_gps[(smooth_gps.key_0 == nearest(cut_gps.index, smooth[smooth['pred'] == 'left'].iloc[0].datetime))]

#let's plot left and right scent makrs on a map
from gmplot import gmplot
smooth_gps.columns

#center map
gmap = gmplot.GoogleMapPlotter(smooth_gps['Latitude'].mean(), smooth_gps['Longitude'].mean(), 13) #lat, log, zoom
gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
#take left and right scent mark coords and plot
points = right.append(left)
gmap.scatter(points.Latitude.values, points.Longitude.values, color='#3B0B39', size=20)
gmap.draw('my_map.html')

#make a map of all locations
gps_all = smooth_gps[np.isfinite(smooth_gps.Latitude)]

gmap = gmplot.GoogleMapPlotter(smooth_gps['Latitude'].mean(), smooth_gps['Longitude'].mean(), 13) #lat, log, zoom
gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
#take left and right scent mark coords and plot
gmap.heatmap(gps_all.Latitude.values, gps_all.Longitude.values)
gmap.scatter(points.Latitude.values, points.Longitude.values, color='#3B0B39', size=2, marker = False)
gmap.draw('my_map.html')