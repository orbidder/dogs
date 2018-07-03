# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 15:43:31 2018

@author: anyke
"""

import pandas as pd
import os

os.chdir('C:\\Data\Hopland Dogs\GPS Data Nate')
filename = 'Nate_20Hz.csv'
nate = pd.read_csv(filename)

nate.head(1)
nate.columns = ['seconds','x','y','z']
nate.set_index('seconds', inplace=True)

twentyHz = nate.iloc[1::2,:]

#twentyHz.to_csv('Nate_Twenty.csv')

twentyHz.head(10).plot()

##Plot in matplotlib
import matplotlib.pyplot as plt

plt.plot(twentyHz.head(1000), color='lightblue', linewidth=3)

plt.show()

#####################################################
#Search for calibration tilts
#change to minutes
twentyHz.index = twentyHz.index/60
twentyHz.index.names = ['minutes']

#for first pass, I did a range of 0 to 1440 (1440 minutes is 24 hours)
#With that, I found the tilts between 132 and 134 minutes
for counter in range(0,1440):
    start = counter*1
    stop = start + 10
    fig = twentyHz[(twentyHz.index > start) & (twentyHz.index < stop)].plot(figsize=(20,10)).get_figure()
    dir_name = 'C:\\Data\Hopland Dogs\GPS Data Nate\explore'
    base_filename = '{0}{1}'.format('output',counter)
    suffix = '.jpg'
    #fig.savefig(os.path.join(dir_name, base_filename + suffix))
    #input("Press Enter to continue...")


#To write this one, I used the original 'seconds' index    
start = 7920
stop = start + 600
twentyHz[(twentyHz.index > start) & (twentyHz.index < stop)].plot(figsize=(20,10))

cut = twentyHz[(twentyHz.index > 7920)]
cut.head(10)

#set seconds to start from 0
cut.index = cut.index-7920
cut.head(10)
cut.to_csv('Twenty_Cut.csv')
print('Done Ow')
