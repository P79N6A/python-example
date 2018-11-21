# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import matplotlib
#导入数据预处理库
from sklearn import preprocessing
from sklearn.preprocessing import Imputer
from sklearn.neural_network import MLPClassifier
#from sklearn.model_selection import GridSearchCV

matplotlib.style.use('ggplot')


def load_data():
    # dataFrame
    df = pd.read_csv('./002362.txt', sep=',', index_col=0)
    # fill the before value
    df.fillna(method='pad')
    df = df.loc[:, ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'DEALNUM', 'PCT_CHG']]
    # 第一行数据去掉
    df = df.iloc[1:df.index.size]
    # 添加一列，累积涨跌幅度
    df.loc[:, 'ACC_PCT_CHG'] = np.array([0] * len(df))
    df.iloc[1:df.index.size, 7] = (df.iloc[1:df.index.size, 3].values-df.iloc[0,3])/df.iloc[0,3]
    # 添加一列，第二天的最高值与前天收盘价比较的涨跌幅度
    #添加一列，第二天的涨跌幅度
    df.loc[:,'TOMORROW_PCT_CHG']=np.array([0] * len(df))
    df.iloc[0:df.index.size - 1, 8]=df.iloc[1:df.index.size,6].values
    #添加一列，第二天的最高值与前天收盘价比较的涨跌幅度
    df.loc[:, 'TOMORROW_HIGH_PCT_CHG'] = np.array([0] * len(df))
    df.iloc[0:df.index.size - 1, 9]=(df.iloc[1:df.index.size,1].values-df.iloc[0:df.index.size-1,3].values)/df.iloc[0:df.index.size-1,3].values
    # 最后一行数据去掉
    df = df.iloc[0:df.index.size-1]
    #print df
    # 查看不同future之间的相关系数
    print "corr:"
    print df.corr()
    # 协方差
    print "cov:"
    print df.cov()
    X = np.array(df.values)
    df=df.loc[:, ['CLOSE']]
    #plt.figure()
    df.plot()
    plt.show()
    print "columns:"
    print df.columns
    return X,df

def pre_process_data(X):
    #print "Nan count:", np.isnan(X)
    print "Nan count:",len(X[np.isnan(X)])
    data=X[:,0:6]

    #process nan value
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp.fit(data)
    data= imp.transform(data)

    #lable
    label=X[:,9]
    label[label >= 0.03] = 1
    label[label <= -0.03] = -1
    label[(label > -0.03) & (label < 0.03)] = 0

    print "data.shape,label.shape",data.shape,label.shape
    return data,label

def split_trainning_(data,label,train_rate):
    training_len=int(label.size*train_rate)
    return data[0:training_len],label[0:training_len],data[training_len:-1],label[training_len:-1]


def scale_data(X_train,X_test):
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    # Don't cheat - fit only on training data
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    # apply same transformation to test data
    X_test = scaler.transform(X_test)
    return X_train,X_test
    # 0-1标准化－－－－范围缩放标准化(0-1 normalization)
    # 范围缩放标准化
    #min_max_scaler = preprocessing.MinMaxScaler()
    # 训练集缩放标准化
    #data = min_max_scaler.fit_transform(data)

def svm_model(x_train,y_train,x_test,y_test):

    best_score=0
    best_C=0
    best_gamma=0

    for cc in [0.1,1,3,10]:
        for ga in [0.001,0.01,0.1,1,10]:
            clf = svm.SVC(probability=True, C=cc, kernel='rbf', gamma=ga,
                          random_state=0, decision_function_shape='ovo')
            clf.fit(x_train, y_train)
            y_predict = clf.predict(x_test)
            score = clf.score(x_test, y_test)
            print 'C,gamma,score:', cc,ga,score
            if(score>best_score):
                best_score=score
                best_C=cc
                best_gamma=ga

    print "best sroce,",best_score,best_C,best_gamma
    clf = svm.SVC(probability=True, C=best_C, kernel='rbf', gamma=best_gamma,
                  random_state=0, decision_function_shape='ovo')
    clf.fit(x_train, y_train)
    y_predict = clf.predict(x_test)
    return y_predict

def svm_predict_optimize(X_train, y_train, X_test, y_test):

    cc = 1
    ga = 10
    testNum = y_test.size
    predict_y = np.empty(testNum)
    data=np.concatenate((X_train, X_test),axis=0) #合并
    label=np.concatenate((y_train,y_test),axis=0) #合并
    #每次都是开始到前一天的所有数据作为训练数据
    for i in range(testNum):
        t_N=data.shape[0]-y_test.shape[0]+i
        # trainData
        training_X, training_y=data[0:t_N],label[0:t_N]
        clf = svm.SVC(C=cc, kernel='rbf', gamma=ga)
        clf.fit(training_X, training_y)
        predict_y[i] = clf.predict(X_test[i])
        print "train.shape,total,i",training_X.shape,testNum,i

    rightNum = len(predict_y[predict_y==y_test])
    print 'score:', rightNum,(rightNum*1.0/testNum)
    return predict_y

# adaboot决策树 预测
def adaboost_predict(X_train, y_train, X_test, y_test):
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.metrics import accuracy_score
    from sklearn.tree import DecisionTreeClassifier
    bdt_real = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=2),
        n_estimators=400,
        learning_rate=1, algorithm='SAMME')
    bdt_real.fit(X_train, y_train)
    y_predict = bdt_real.predict(X_test)
    score = bdt_real.score(X_test, y_test)
    print 'score:', score
    return y_predict

def nnm_multi_layer_perception(X_train, y_train, X_test, y_test):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
    clf.fit(X_train,y_train)
    y_predict=clf.predict(X_test)
    score=clf.score(X_test,y_test)
    print 'score:', score
    return y_predict

def see_predict_detail(y_train,y_test,y_predict):
    dedup_label=set(y_train)
    for y in [y_train,y_test,y_predict]:
        for item in dedup_label:
            print item,":",len(y[y == item]),",",
        print ""

    # 测试效果详情
    from sklearn import metrics
    print(metrics.classification_report(y_test, y_predict))
    print metrics.confusion_matrix(y_test, y_predict)

def select_model_predict(X_train, y_train, X_test, y_test, model='svm'):
    if (model == 'svm'):
        return svm_model(X_train, y_train, X_test, y_test)
    elif (model == 'ada'):
        return adaboost_predict(X_train, y_train, X_test, y_test)
    elif (model=='svm_o'):
        return svm_predict_optimize(X_train, y_train, X_test, y_test)
    elif (model=='nnm'):
        return nnm_multi_layer_perception(X_train, y_train, X_test, y_test)
    else:
        print "ERROR type for ", model


def main():
    X,df=load_data()
    data,label=pre_process_data(X)
    x_train, y_train, x_test, y_test=split_trainning_(data,label,0.8)
    x_train,x_test=scale_data(x_train,x_test)
    y_predict=select_model_predict(x_train, y_train, x_test, y_test,'svm_o')
    see_predict_detail(y_train,y_test,y_predict)

main()