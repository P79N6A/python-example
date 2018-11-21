# -*- coding: utf-8 -*-

from sklearn import preprocessing
from sklearn.preprocessing import Imputer
import numpy as np


# Standardization of datasets is a common requirement for many machine learning estimators
# implemented in scikit-learn

# Scaled data has zero mean and unit variance
#f your data contains many outliers 极端值,
# scaling using the mean and variance of the data is likely
# to not work very well.
def scale(X):
    return preprocessing.scale(X)


# convert to 0~1
def minMaxScaler(X):
    min_max_scaler = preprocessing.MinMaxScaler()
    X_train_minmax = min_max_scaler.fit_transform(X)
    return X_train_minmax

#This assumption is the base of the Vector Space Model often used in text classification and clustering contexts.
#The function normalize provides a quick and easy way to perform this operation on a single array-like dataset,
# either using the l1 or l2 norms:
def normalize(X):
    X_normalized = preprocessing.normalize(X, norm='l2')
    return X_normalized

#The following snippet demonstrates how to replace missing values, encoded as np.nan,
# using the mean value of the columns (axis 0) that contain the missing values:
def imputerWithMean(X):
   imp= Imputer(missing_values='NaN',strategy='mean',axis=0)
   imp.fit(X)
   return imp.transform(X)

#test
def main():
    X_train = np.array([[1., -1., 2.],
                        [2., 0., 0.],
                        [0., np.nan, -1.]])

    X_train=imputerWithMean(X_train)
    print 'Nan to mean',X_train
    X=minMaxScaler(X_train)
    print X

    Y=np.array([[1,2,3],
                [3,5,2],
                [7,2,0],
                [2,3,7]])
    Y_train=Y[0:3]
    Y_test=Y[3:]
    min_max_scaler = preprocessing.MinMaxScaler()
    YY = min_max_scaler.fit_transform(Y)
    print "all", YY
    print "Y",Y_test

    min_max_scaler2=preprocessing.MinMaxScaler()
    Y_train=min_max_scaler2.fit_transform(Y_train)
    Y_test=min_max_scaler2.fit_transform(Y_test)
    print "split:",Y_train,Y_test
main()