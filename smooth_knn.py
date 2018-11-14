# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:09:33 2018
Smoothing predicted classes
From Supp Inf
8.	Use the smooth_knn.py script to smooth the KNN predictions to 1 Hz so that they can 
be linked to GPS locations recorded at that time. This script takes the 25 Hz accelerometer 
data and smooths it to 1 Hz, by taking the modal class for each 25-row group that constitutes 
a second of accelerometer data. There is also a function in this script to check each class' 
accuracy and ensure the smoothed data matches the actual classes as recorded by video (after 
those annotations too has been smoothed).
@author: Owen R. Bidder
"""
import pandas as pd
import numpy as np
import os
os.chdir('C:\\DataFolder\...') #Data location here

#Load in annotated accl data
accl_data = pd.read_csv('dog_actual_pred.csv') #data with actual and predicted classes from behavioural validation period 
accl_data.set_index('seconds', inplace=True)
accl_data['r_secs'] = np.around(accl_data.index, decimals = 0) #define the second epoch across which all sub-second data will be smoothed

#produce a downsampled (to 1 Hz) dataset, take the modal class from each second
smooth = pd.DataFrame(index = np.around(accl_data.index, decimals = 0).unique())
smooth['actual'] = accl_data.groupby('r_secs')['class'].agg(lambda x:x.value_counts().index[0])
smooth['pred'] = accl_data.groupby('r_secs')['pred_class'].agg(lambda x:x.value_counts().index[0])


# Let's plot predicted activity and actual activity
#Predicted
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(smooth.index, smooth['pred'], 'o')

ax.set(xlabel='time (s)', ylabel='behavior',
       title='Predicted Activity - Dog')
ax.grid()
plt.show()
#fig.savefig("predicted.png")

#Actual
fig, ax = plt.subplots()
ax.plot(smooth.index, smooth['actual'], 'o')

ax.set(xlabel='time (s)', ylabel='behavior',
       title='Actual Activity - Dog')
ax.grid()
plt.show()
#Looks pretty good, let's make sure our scent marks are being detected decently

#run quick accuracy check
def check(x, y):
    if len(x) == len(y):
        x = np.array(x)
        y = np.array(y)
        xy = np.where(y == x, 1, 0)
    else:
        dfx = pd.DataFrame(x)
        dfy = pd.DataFrame(y)
        df = dfx.merge(dfy, how='outer', on='seconds')
        df['cor'] = np.where(df.pred == df.actual, 1, 0)
        xy = df['cor']
    return np.mean(xy)

check(smooth['actual'],smooth['pred']) # 95.5% accuracy on the whole

#Can perform behaviour specific accuracy calculations here if you wish
#check(smooth['pred'][smooth.pred == 'right'],smooth['actual'][smooth.actual == 'right']) # 
#check(smooth['pred'][smooth.pred == 'left'],smooth['actual'][smooth.actual == 'left']) # 
#check(smooth['pred'][smooth.pred == 'scent'],smooth['actual'][smooth.actual == 'scent']) # 85.7% accuracy for left
#check(smooth['pred'][smooth.pred == 'lie'],smooth['actual'][smooth.actual == 'lie']) #99%
#check(smooth['pred'][smooth.pred == 'stand'],smooth['actual'][smooth.actual == 'stand']) #77%

#Check accuracy, seems pretty good, export smooth data ready to be synced to GPS
smooth.to_csv('dog_smooth_accl.csv')

#Run smoothing over the unobserved period predictions too
#Load in annotated accl data
dog_unobs = pd.read_csv('dog_unobs_predicted.csv') #file containing unobserved predictions, from KNN_sm.py
dog_unobs.set_index('seconds', inplace=True)
dog_unobs.head(10)
dog_unobs['r_secs'] = np.around(jas_unobs.index, decimals = 0)
dog_unobs.head(10)

#produce a downsampled (to 1 Hz) dataset, take the modal class from each second
smooth_unobs = pd.DataFrame(index = np.around(dog_unobs.index, decimals = 0).unique())
smooth_unobs['pred'] = dog_unobs.groupby('r_secs')['pred_class'].agg(lambda x:x.value_counts().index[0])
smooth_unobs.head(10)
smooth_unobs.to_csv('dog_unobs_smooth_preds.csv') #write out the 1 Hz predictions, ready to be linked to GPS data
