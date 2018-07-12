# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:09:33 2018
Smoothing predicted classes
@author: Owen R. Bidder
"""
import pandas as pd
import numpy as np
import os
os.chdir('C:\\Data\Hopland Dogs\GPS Data Nate')

#Load in annotated accl data
accl_data = pd.read_csv('nate_actual_pred.csv')
accl_data.set_index('seconds', inplace=True)
accl_data['r_secs'] = np.around(accl_data.index, decimals = 0)

#produce a downsampled (to 1 Hz) dataset, take the modal class from each second
smooth = pd.DataFrame(index = np.around(accl_data.index, decimals = 0).unique())
smooth['actual'] = accl_data.groupby('r_secs')['class'].agg(lambda x:x.value_counts().index[0])
smooth['pred'] = accl_data.groupby('r_secs')['pred_class'].agg(lambda x:x.value_counts().index[0])

#smooth['actual'].unique()
#classes = {'no_class' : 1, 'walk' : 2, 'left' : 3, 'run' : 4, 'jump' : 5, 'stand' : 6, 'lie' : 7, 'right' : 8}

# Let's plot predicted activity and actual activity
#Predicted
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(smooth.index, smooth['pred'], 'o')

ax.set(xlabel='time (s)', ylabel='behavior',
       title='Predicted Activity - Nate')
ax.grid()
plt.show()
#fig.savefig("predicted.png")

#Actual
fig, ax = plt.subplots()
ax.plot(smooth.index, smooth['actual'], 'o')

ax.set(xlabel='time (s)', ylabel='behavior',
       title='Actual Activity - Nate')
ax.grid()
plt.show()
#Looks pretty good, let's make sure out scent marks are being detected decently

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

check(smooth['actual'],smooth['pred']) # 93% accuracy on the whole

check(smooth['pred'][smooth.pred == 'right'],smooth['actual'][smooth.actual == 'right']) # 83% accuracy for right
check(smooth['pred'][smooth.pred == 'left'],smooth['actual'][smooth.actual == 'left']) # 0.75% accuracy for left
check(smooth['pred'][smooth.pred == 'lie'],smooth['actual'][smooth.actual == 'lie']) #98%
check(smooth['pred'][smooth.pred == 'stand'],smooth['actual'][smooth.actual == 'stand']) #93%

#Check accuracy, seems pretty good, export smooth data ready to be synced to GPS
smooth.to_csv('smooth_accl.csv')

