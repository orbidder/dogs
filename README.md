# dogs
NOTICE: If this is the first time you're visiting this repository, take a look at KNN.R for a worked example of K-nearest neighbour on accelerometer data.

All files for classification of canid accelerometer data to identify scent marks

UPDATE: 7/3/2018
Owen B:

I've been working through the first of the Hopland dog's data, Nate. I've started putting a workflow that is summarized briefly here.

Validation using camera observation period

1. Use OMGui to convert the .cwa files in to a resampled .csv . I found it was useful to downsample tha acclerometer data to 25Hz, as these files are more easily handled.

2. Do a quick summary plot using the crop_spyder.py, if the file is too large, you can cut out just the first n number of rows to get just the time during which we filmed the dogs

3. Use subsample.py to plot 10 minute summaries of the data. The function will run through the first 3 days of the file (after that the tag was off the animal and so it's just excess data), showing 10 minutes at a time to help you find the calibration tilts we placed at the start of the accl and video in order to sync the two. This function needs there to be a folder called 'explore', which will be filled with plots for you to run through sequentially. I couldn't think of a more elegant way to do this, but if someone finds a plotting function that's scrollable, we can edit it in. Once you know where the tilts are, I suggest you trim the start of the file to ~5 seconds before the tilts to make it easy to sync in ELAN

4.Load the trimmed data in to ELAN, along with the video. Sync the two using the procedure detailed in this video: https://www.youtube.com/watch?v=zofLvUU0Gus
Then just run through the video and make annotations, output annotations as a tab delimited text file

5.Load the accelerometer data and the annotation record, combine the two using the label_accl.py script. This will output a accl file with an extra column that contains the class of behaviour being undertaken by the animal at that time

6.Use the KNN_Nate.py script to actually train and test the KNN classifier to the annotated data. Doing this process with Nate's data has highlighted the need to run another filter over Nate's KNN output, because this dog doesn't raise its legs very high, so stand, scent marks and lying are often confused. I suggest a duration filter that says 'if the activity (scent mark/stand/lying) last under 6 seconds, it's a scent mark, over 6 s is a stand, and anything 15-1000s is probably lying down or resting. This isn't ideal but Nate didn't behave like the Norwegian Dogs in the validation study.
