# dogs
NOTICE: If this is the first time you're visiting this repository, take a look at KNN.R for a worked example of K-nearest neighbour on accelerometer data.

Directions for use of Python scripts
To encourage uptake of the methods described in this study, we have provided all of the scripts necessary to implement detection of scent-marking detection in accelerometer data, and link those detected events to GPS data collected concurrently. Some devices may produce data files that follow a different format, but the code here should be general enough to implement for most devices with some minor adjustment to the code. Here we present a brief outline of the workflow when using these scripts.

1.	When using the AX3 accelerometer, use OMGui (https://github.com/digitalinteraction/openmovement/wiki/AX3-GUI) to convert the .cwa files in to a resampled CSV file. We down-sampled data to 25 Hz to improve computation speed.

2.	Do a quick summary plot using the crop_file.py. We used this script to crop the file, as the device continued to record after it was removed from the dogs, producing large files with superfluous data. Use the ‘chunksize’ argument to specify how many rows should be taken from the start of the file.

3.	Before we can use the KNN to predict scent-marking events, we need to use an initial period of observation to train the model. In our study, we obtained a training set by observing the dog prior to release. Thus, the accelerometer file must be split in to training and testing periods. The next few steps detail how one may prepare and train the KNN.

4.	We must synchronize the timestamp of the accelerometer data with the video that details to behavioural observations of the dog. At the beginning of the observation period, we performed conspicuous calibration tilts (the device was rotated 90 degrees for 5 second, and this was repeated 3 times). With this in mind, use subsample.py to plot 10-minute summaries of the data. The function will run through the first 3 days of the file (after that the tag was off the animal and so it's just excess data), showing a 10 minute window in each plot to help you find the calibration tilts mentioned previously. This function needs there to be a folder called 'explore', which will be filled with plots for you to run through sequentially (using Windows’ Photo app for instance). In future, we will implement a more elegant interactive plot for Users to use in Python, but this is currently in development. Once the tilts are identified and their time in the accelerometer file noted, you can trim the start of the file to ca. 5 seconds before the tilts, to make them easy to spot and sync to the video in ELAN.

5.	Load the trimmed data in to ELAN, along with the video. Sync the two using the procedure detailed in the video tutorial kindly produced by Cassim Ladha (https://www.youtube.com/watch?v=zofLvUU0Gus). Then run through the video and make annotations. Following this, output annotations as a tab delimited text file to load back in to Python.

6.	Using the label_accl.py script, load the accelerometer data and the annotation record, combine the two to produce one annotated accelerometer dataset. This will output an accelerometer file with an extra column that contains the class of behaviour being undertaken by the animal at that time.

7.	Use the KNN_sm.py script to actually train and test the KNN classifier to the annotated data. Functions to obtain performance metrics (e.g. Accuracy) are included, along with a means to construct confusion matrices to evaluate the KNN’s performance.

8.	Use the smooth_knn.py script to smooth the KNN predictions to 1 Hz so that they can be linked to GPS locations recorded at that time. This script takes the 25 Hz accelerometer data and smooths it to 1 Hz, by taking the modal class for each 25-row group that constitutes a second of accelerometer data. There is also a function in this script to check each class' accuracy and ensure the smoothed data matches the actual classes as recorded by video (after those annotations too has been smoothed).

9.	Using the link_gps.py script, merge the predicted classes of the accelerometer data (a product of the KNN) to the Latitude and Longitude values in the GPS data. Once the GPS data has behavioural classes, identify the points where dogs are making left and right scent marks. These points then can be written to file for use in GIS software or R for further analysis.

10.	These steps can then be repeated using data from the unobserved period (obtained during deployment on free living animals for instance) to obtain a record of scent-marking locations. The necessary code segments are presented in the scripts above too.

