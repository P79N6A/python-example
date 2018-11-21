# -*- coding: utf-8 -*-
print(__doc__)
'''
使用scikit－learn 线性SVM对数据两分类，并plot制图 
'''
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm


def loadDataSet(fileName):
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat


# we create 40 separable points
#np.random.seed(0)
#X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]
#Y = [0] * 20 + [1] * 20

X,Y=loadDataSet('svmMLiA.txt')
X=np.array(X)
Y=np.array(Y)
# fit the model
clf = svm.SVC(kernel='linear')
clf.fit(X, Y)

# get the separating hyperplane:y=wx+b
w = clf.coef_[0]
a = -w[0] / w[1]
xx = np.linspace(-2, 10,10) # 针对数据生成一些x点，用于画线
yy = a * xx - (clf.intercept_[0]) / w[1]

# plot the parallels to the separating hyperplane that pass through the
# support vectors
b = clf.support_vectors_[0]
yy_down = a * xx + (b[1] - a * b[0])  # move line
b = clf.support_vectors_[-1]
yy_up = a * xx + (b[1] - a * b[0])   #move line

# plot the line, the points, and the nearest vectors to the plane
plt.plot(xx, yy, 'k-')
plt.plot(xx, yy_down, 'k--')
plt.plot(xx, yy_up, 'k--')

plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
            s=80, facecolors='red')
plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired)

plt.axis('tight')
plt.show()