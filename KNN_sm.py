# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 11:27:55 2018
KNN analysis of annotated accl data

From Supp Inf
7.	Use the KNN_sm.py script to actually train and test the KNN classifier to 
the annotated data. Functions to obtain performance metrics (e.g. Accuracy) are 
included, along with a means to construct confusion matrices to evaluate the KNN’s performance.
@author: Owen R. Bidder
"""
import pandas as pd
import os
os.chdir('C:\\DataFolder\...') #Data location here

#Load in annotated accl data
accl_data = pd.read_csv('dog_annot_accl.csv') #from label_accl.py
accl_data.set_index('seconds', inplace=True) #set the index

#remove all calibration stuff, and data that wasn't labelled at the start of the file
accl_data = accl_data[accl_data['class'] != 'calibration']

#set x (accl data) and y (classes)
x = accl_data.iloc[:,1:4]
y = accl_data['class']

#Split accl_data to testing and training sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42, shuffle=True)

#check training and testing have the same classes in them
set(y_train) == set(y_test)

## Import the KNN Classifier.
from sklearn.neighbors import KNeighborsClassifier
## Start the KNN instance, setting k to 5 neighbors. 
knn = KNeighborsClassifier(n_neighbors=5)
## Fit the model on the training data.
knn.fit(X_train, y_train.values.ravel())
## See how the model performs on the test data.
knn.score(X_test, y_test) #This is the accuracy

##Get Array of all predictions
y_pred = knn.predict(X_test)

##Calculate confusion matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score

confusion_matrix(y_test, y_pred)
accuracy_score(y_test, y_pred) #Accuracy
cohen_kappa_score(y_test, y_pred) #Cohen's Kappa

##Plot a confusion matrix
import itertools
import numpy as np
import matplotlib.pyplot as plt

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

##Get confusion matrix    
cnf_matrix = confusion_matrix(y_test, y_pred)
class_names = y_test.unique()

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')

plt.show()

##Build classification report
from sklearn.metrics import classification_report
#target_names = ['class 1', 'class 2', 'class 3', 'class 4']
print(classification_report(y_test, y_pred, target_names=class_names))

##Join x_test and y_pred for output
output = X_test
output['class'] = y_pred
output.sort_index(inplace = True)
output.to_csv('dog_pred_output.csv')

#plot output
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

# Let's plot predicted activity and actual activity
#Predicted
fig, ax = plt.subplots()
ax.plot(output.index, output['class'], 'o')

ax.set(xlabel='time (s)', ylabel='behavior',
       title='Predicted Activity - Nate')
ax.grid()
plt.show()
#fig.savefig("predicted.png")

#Actual
fig, ax = plt.subplots()
ax.plot(accl_data.index, accl_data['class'], 'o')

ax.set(xlabel='time (s)', ylabel='behavior',
       title='Actual Activity - Nate')
ax.grid()
plt.show()
#fig.savefig("actual.png")

#perform a full prediction
accl_data['pred_class'] = knn.predict(accl_data.iloc[:,1:4])
accl_data
knn.score(accl_data.iloc[:,1:4], accl_data['class']) #92.6%
accl_data.to_csv('dog_actual_pred.csv')


#Here we predict activity during the unobserved period (from full deployment etc.) 
#using the KNN that has been trained and validated above
dog_unobs = pd.read_csv('dog_unobserved.csv') #from label_accl.py script
dog_unobs.set_index('seconds', inplace=True)
dog_unobs.head(10)
dog_unobs['pred_class'] = knn.predict(dog_unobs.iloc[:,1:4])
dog_unobs.head(10)
dog_unobs.to_csv('dog_unobs_predicted.csv')

#KNN finished, now use smooth_knn.py to prepare predictions for matching with GPS data