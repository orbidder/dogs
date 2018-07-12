# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:38:52 2018

@author: Owen
"""
# This file is to annotate the accl data using the annotation record from ELAN
import pandas as pd
import os

# Load accl data and set time to start from the first calibration point
os.chdir('C:\\Data\Hopland Dogs\GPS Data Nate')
filename = 'Twenty_Cut.csv'
twentyHz = pd.read_csv(filename)

twentyHz.columns = ['seconds', 'x', 'y', 'z']
twentyHz.set_index('seconds', inplace=True)

# Elan says the offset was 24.666 seconds, so plot to make sure and then cut
start = 24.65
stop = start + 5
twentyHz[(twentyHz.index > start) & (twentyHz.index < stop)].plot(figsize=(10, 5))

# from annotation, we can see the video ends at 2813.644
# cut file to duration of video
twentyHz = twentyHz[(twentyHz.index > start) & (twentyHz.index < 2813.64)]
# set start time to 0
twentyHz.index = twentyHz.index - twentyHz.index[0]

# now load in annotations
annot = pd.read_table('Nate_Annotate.txt', delimiter="\t", header=None)
annot.columns = ['class', 'nans', 'start', 'end', 'duration', 'text']
annot.start.iloc[0] = 0.0

# add column to put our annotations
import numpy as np

twentyHz['class'] = np.nan

#twentyHz.to_csv('twenty_for_par.csv')
# this is debug code, skip to function
# row = twentyHz.loc[twentyHz.index == 539.5040000000009].iloc[0,]
# time = row.name
# lab_class = annot[(annot['start'] <= time) & (annot['end'] >= time)]['class']
# if len(lab_class.index) == 0:
#    row['class'] = 'no_class'
# else:
#    row['class'] = lab_class
# row

# twentyHz.loc[(twentyHz.index < 539.498) & (twentyHz.index > 539.393)].index[0]

def label(accl_data):
    time = accl_data.name
    lab_class = annot[(annot['start'] <= time) & (annot['end'] >= time)]['class']
    if len(lab_class.index) == 0:
        accl_data['class'] = 'no_class'
    else:
        accl_data['class'] = lab_class.iloc[0]
    return accl_data;


label(twentyHz.iloc[0,])

#%timeit test = twentyHz.apply(label,axis=1)
import time
t0 = time.perf_counter()
test = twentyHz.apply(label,axis=1)
test.to_csv('annotated_accl.csv')
t1 = time.perf_counter()
total = t1-t0


###The code below works much much faster to label twentyHz rows with class infro from annot
# I was able to do it using help from some folks on the internet!

import pandas as pd
import numpy as np
import time
# Create mock dfs
#twentyHz = pd.DataFrame(np.random.randn(20, 3).round(), columns=list('abc'))
#annot = pd.DataFrame({'start': [0, 4, 7, 12, 15], 'end': [3, 6, 9, 15, 17], 'class': ['A', 'B', 'B', 'C', 'D']})

t0 = time.perf_counter()
bins = np.unique(annot[['start', 'end']].values.flatten())  # get time range bins
annot['period'] = '['+annot['start'].astype(str) + ', ' + annot['end'].astype(str) + ')'
categorized = pd.cut(twentyHz.index, bins, right=False).astype(str) # categorize into bins based on time, right=False means start is inclusive, end is exclusive
categorized = pd.Series(categorized).to_frame('labels') # make it a dataframe to get ready for merge below
twentyHz['class'] = categorized.merge(annot, left_on='labels', right_on='['+annot['start'].round(decimals=3).astype(str) + ', ' + annot['end'].round(decimals=3).astype(str) + ')', how='left')['class'].fillna('no class').values # merge with processed annot frame to get the correct labels

t1 = time.perf_counter()
total = t1-t0
twentyHz.to_csv('annotated_accl.csv')

print('Done Ow')
