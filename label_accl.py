# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:38:52 2018
From Supp Inf
6.	Using the label_accl.py script, load the accelerometer data and the annotation record, 
combine the two to produce one annotated accelerometer dataset. This will output an accelerometer 
file with an extra column that contains the class of behaviour being undertaken by the animal at that time.
@author: Owen R Bidder
"""
# This script is to annotate the accl data using the annotation record from ELAN
import pandas as pd
import os

# Load accl data and set time to start from the first calibration point
os.chdir('C:\\DataFolder\...') #Data location here
filename = 'dog_df_Cut.csv' #the output from subsample.py
twentyHz = pd.read_csv(filename)

twentyHz.set_index('seconds', inplace=True)

# In this example, ELAN said the offset was 21 seconds, so plot to make sure and then cut
start = 20.6
stop = start + 40
twentyHz[(twentyHz.index > start) & (twentyHz.index < stop)].plot(figsize=(10, 5))

# from annotation, we can see the video ends at 31 minutes, 1.653 seconds
# that's 1861.653 seconds long

# For later use, create csv for the unobserved period that begins immmediately at the end of the video
df_unobs = twentyHz[(twentyHz.index > 1861.653)]
df_unobs.iloc[::20, :].iloc[:,0:4].plot() #quickly plot every 20th row to get a summary of file


#I will pass all data through KNN and then cut the end according to the timestamp
df_unobs.to_csv('dog_unobserved.csv') #a file that contains only unobserved data, from free living deployments etc.

# cut another file to duration of video for KNN training and validation
twentyHz = twentyHz[(twentyHz.index > start) & (twentyHz.index < 1861.653)]
# set start time to 0
twentyHz.index = twentyHz.index - twentyHz.index[0]

# now load in annotations
annot = pd.read_table('dog_Annotate.txt', delimiter="\t", header=None)
annot.columns = ['class', 'nans', 'start', 'end', 'duration', 'text'] #the columns typically output from ELAN
annot.start.iloc[0] = 0.0

# add column to put our annotations
import numpy as np

twentyHz['class'] = np.nan #fill with NaN for now

#The following code takes the behavioural record from annot and uses them to populate the 'class' column in twentyHz
import pandas as pd
import numpy as np
import time

bins = np.unique(annot[['start', 'end']].values.flatten())  # get time range bins
annot['period'] = '['+annot['start'].astype(str) + ', ' + annot['end'].astype(str) + ')'
categorized = pd.cut(twentyHz.index, bins, right=False).astype(str) # categorize into bins based on time, right=False means start is inclusive, end is exclusive
categorized = pd.Series(categorized).to_frame('labels') # make it a dataframe to get ready for merge below
twentyHz['class'] = categorized.merge(annot, left_on='labels', right_on='['+annot['start'].round(decimals=3).astype(str) + ', ' + annot['end'].round(decimals=3).astype(str) + ')', how='left')['class'].fillna('no class').values # merge with processed annot frame to get the correct labels


twentyHz.to_csv('dog_annot_accl.csv') #this accelerometer file now has behavioural annotations for use in the KNN

print('Script Finished')