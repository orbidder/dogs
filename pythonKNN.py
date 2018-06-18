# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 10:49:24 2018
KNN for accelerometers
@author: Owen
"""
import pandas as pd
import os

os.getcwd()
os.chdir('C:\\Data\Hopland Dogs\\Norway Dogs')

## Load in all data
col_names = ['X', 'Y', 'Z']
X_test = pd.read_csv('test1.csv', header=None, names=col_names)

X_train = pd.read_csv('train1.csv', header=None, names=col_names)

y_train = pd.read_csv('classes1.csv', header=None, names=['class'])

y_test = pd.read_csv('testclasses.csv', header=None, names=['class'])

## Import the Classifier.
from sklearn.neighbors import KNeighborsClassifier
## Instantiate the model with 5 neighbors. 
knn = KNeighborsClassifier(n_neighbors=5)
## Fit the model on the training data.
knn.fit(X_train, y_train.values.ravel())
## See how the model performs on the test data.
knn.score(X_test, y_test)

##Get Array of all predictions
y_pred = knn.predict(X_test)

##Calculate confusion matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score

confusion_matrix(y_test, y_pred)
accuracy_score(y_test, y_pred)
cohen_kappa_score(y_test, y_pred)

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
class_names = y_test['class'].unique()

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
target_names = ['class 1', 'class 2', 'class 3', 'class 4']
print(classification_report(y_test, y_pred, target_names=target_names))
