# -*- coding: utf-8 -*-
from sklearn import svm
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.datasets import samples_generator
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import pandas as pd


X, y = samples_generator.make_classification(
    n_informative=5, n_redundant=0, random_state=42)


# 数据预处理
min_max_scaler = preprocessing.MinMaxScaler()

#grid serarch
parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10],'gamma':[1,2]}
clf = GridSearchCV(svm.SVC(), parameters)

#pipeline
pre_svm = Pipeline([('min_max', min_max_scaler), ('svc', clf)])

#pre_svm.set_params(min_max__feature_range=(0, 1),svc__C=2).fit(X,y)
pre_svm.fit(X,y)

print pre_svm
print "best parameter:",clf.best_params_
df=pd.DataFrame(clf.cv_results_)
print df

prediction = pre_svm.predict(X)
print pre_svm.score(X, y)
print(metrics.classification_report(y, prediction))
print metrics.confusion_matrix(y, prediction)





