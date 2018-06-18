####################################################################################################
#This script runs K nearest neighbour analysis on files "train1.txt" and "test1.txt"
#Data files should be in .txt format, with each accelerometer axis in its own column, no spaces in between.
#Axis order (e.g. X,Y,Z etc..) is unimportant provided it is consistent between training and testing files
#The behavioural labels of the training set should be saved into a .txt file with a single column
#The label order should correspond to the accelerometer data in the training file
library(stats)
library(class)

#load up train and testing files
train1 = scan("train1.txt") 
test1 = scan("test1.txt")

#convert inputs into matrix
train1 = matrix(train1, byrow = T, ncol=3)
test1 = matrix(test1, byrow = T, ncol=3)

#load the classes in the training data
cl1a = scan("classes1.txt")

#set k 
kk = 21

#run knn
kn1 = knn(train1, test1, cl1a, k=kk, prob=TRUE)

prob = attributes(.Last.value)
clas1=factor(kn1)

#write results, this is the classification of the testing set in a sinlge column
filename = paste("resultstrial", kk, ".csv", sep="")
write.csv(clas1, filename)

#write probs to file, this is the proportion of k nearest datapoints that contributed to the winning class
fileprobs = paste("probstrial", kk, ".csv", sep="")
write.csv (prob$prob, fileprobs)

##############################################################################################
#The next part of the script runs a filter over the results, accepting the classification made
# by the KNN, provided the 'prob' value meets a certain threshold value (which can be defined).
#This can increase the precision of the KNN method, accepting classifications only when we are confident
# that they are correct. Prob values reflect the proportion of the k-nearest neighbours that were in the winning
# class. So classifications with a low majority of k-nearest data in the winning class are discarded.

#First we define our minimum majority threshold value
thres <- 0.7

#We load back in the results and prob values and combine them into a matrix with 2 columns
results = read.csv("resultstrial21.csv", header = TRUE)
probs = read.csv("probstrial21.csv", header = TRUE)
resprob = cbind(results$x, probs$x)

#Now "resprob" has two columns, V1 contains the classifications, V2 the prob values. Now let's apply
# the threshold to the prob values, making a new column containing 1 if it meets the threshold
# and 0 if it doesn't.

#First let's make resprob a data frame
resprob = as.data.frame(resprob)

#Then we apply the threshold, filling in a thirdcolumn "V3"
resprob$V3 = resprob$V2 >= thres

#or you can use the following; res$V3 <- ifelse(res$V2 >= .7, 1, 0)
#this uses the ifelse command, which works like this: ifelse(condition, do_if_true, do_if_false)


#Save resprob to a file to look at later
write.csv(resprob, "resprob.csv")



#############################################################################################
#In this section we plot the accl data on an XYZ scatterplot in order to show the clustering
# and how classifications were made by the KNN

#Make a new data frame for plotting, with test1 data and the resprob data too.
test1 <- as.data.frame(test1)
forplot <- cbind(test1$V1, test1$V2, test1$V3, resprob$V1, resprob$V2, resprob$V3)

#Delete any row of data for which the prob value didn't meet the minimum threshold
forplot <- as.data.frame(forplot)
jtso <- forplot[!forplot$V6 == 0, ]

#Plot all the data that was classed in an XYZ scatterplot, colour the data according to class
#split the data frame according to the classes in column V4. Mylist 1 is class 1, mylist 2 is class 2 etc..
mylist <- split(jtso, jtso$V4)
mylist[[1]]

#now lets plot the data coloured according to class
install.packages("scatterplot3d")
library(scatterplot3d)


##This plot can compare 3 series, which are the elements in mylist##
file1 <- mylist[[1]]
file2 <- mylist[[2]]
file3 <- mylist[[3]]
s3d <- scatterplot3d(file1$V1, file1$V2, file1$V3, main= "3D Scatterplot of all behaviour classes", color = "blue", xlab = "X accl", ylab = "Y accl", zlab = "z accl", xlim = c(-2,2), ylim = c(-2,2), zlim = c(-2,2))
s3d$points3d(file2$V1, file2$V2, file2$V3, col = rgb(0,1,0,))
s3d$points3d(file3$V1, file3$V2, file3$V3, col = rgb(1,0,0,))
legend(s3d$xyz.convert(2,-0.2,1.8), col= c("blue", "green", "red"),
       legend = c("Class 1", "Class 2", "Class 3"), lwd = 2,
       bg = "white")

###################################################################################
#In this section we will make an XY plot showing time on the x-axis and the class on the y-axis#
#This can be used in interpretation of the behavioural data#

#Include the time data  for the test file, which are contained in a file called "times.csv"
#the time stamp data are in a single column, cut from the original file prior to conducting the KNN
times <- read.csv("times.csv", header = FALSE)
#options(digits.secs = 3)
#times <- strptime(times,"%M:%OSn")
#times

#create a new data frame with times, accl data from 'forplot', classes from 'forplot' and a column
# of whether or not that classification met the threshold. Using cbind.data.frame ensures it is treated
# as a data frame and data from times are pasted into the new frame as they appear in 'times'
timeplot <- cbind.data.frame(times$V1, forplot$V1, forplot$V2, forplot$V3, forplot$V4, forplot$V6)
#Rename the columns for ease of use later
names(timeplot)[1] <- "V1"
names(timeplot)[2] <- "V2"
names(timeplot)[3] <- "V3"
names(timeplot)[4] <- "V4"
names(timeplot)[5] <- "V5"
names(timeplot)[6] <- "V6"

#Filter rows that didn't meet the threshold from 'timeplot'
timeplot <- timeplot[!timeplot$V6 == 0, ]
#plot as XY plot with time on x-axis and the class on the y-axis
plot(timeplot$V1, timeplot$V5)
#You can now get a timeline with all the behavioural classes and the sequence in which they occur, or use
# timeplot data frame to calculate the durations for which behaviours occur etc.

##############################################################################################
#In this section we will compare the results of the KNN to the known classifications of the testing set
# This will allow us to calculate accuracy, precision and recall for the KNN on this data set
# This can be used to run a validation experiment, similar to the one in the PLoS One paper by Bidder et al.

#We need the known classifications of the testing set for this part of the analysis. Like those for the 
# training set, the classes of the testing set should be in a .txt file, in a single column.
# Here they are saved in a file called "testclasses.txt. 
library(caret)
#Load the classes from the "testclasses.txt" file.
testclasses = read.csv("testclasses.csv", header = F)
testclasses <- testclasses[,1]

#We use the predictions from the KNN conducted earlier, but as a numeric to match the testclasses object class
predclasses <-as.numeric(clas1)

#using the caret library, we compare predicted with actual classes and 
#construct a confusion matrix to calculate accuracy etc.
conf <- confusionMatrix(predclasses,testclasses)

conf #look at results

