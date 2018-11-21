# -*- coding: utf-8 -*-
'''
author:zhoupj
date:20170613
'''
import scipy.io as sio
import matplotlib.pyplot as plt
import sklearn.svm as svm
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve, auc
from scipy import interp
from itertools import cycle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
#导入数据预处理库
from sklearn import preprocessing


#  20050105_20160909 的日频率数据
def loadData():
    filename = '../SVM_codes_final/Factor_adaboost_General_000905_updateeveryday.mat'
    data = sio.loadmat(filename)
    # 时间轴
    datelist_Factor_000905 = data.get('datelist_Factor_000905')
    # 大盘因子时间序列，每行为不同的因子，每列与datelist_Factor_000905相对应，每列在时间轴上那天开盘前可以得到。
    # 62 个因子
    factor_000905 = data.get('Factor_000905')
    # 转置,1行62个特征
    factor_000905 = factor_000905.transpose()
    # 中证500收益率序列，与Factor_000905和datelist_Factor_000905向前对应，是对应时间轴上收盘后得到的当天收益率（收盘 - 前收）
    return_000905 = data.get('Return_000905')
    # 转置.列向量
    return_000905 = return_000905.transpose()

    #
    return datelist_Factor_000905, factor_000905, return_000905


# 对数据进行过滤处理，处理nan，inf等数据，处理不合理的因子
def filterData(dataArr, label, typeNum=2):
    ori_label = label
    m, n = dataArr.shape
    fiterCol = np.zeros((n), dtype=bool)
    for i in range(n):
        nanNum = np.count_nonzero(dataArr[:, i] != dataArr[:, i])
        if (nanNum > 100):
            print "nan num >100", i, nanNum
            fiterCol[i] = False
        else:
            fiterCol[i] = True
    # 因子数量nan数量太多的则舍弃，不再当作因子（特征）
    newData = dataArr[:, fiterCol]
    print "nan data len", len(newData[np.isnan(newData)])
    # newData[np.isnan(newData)] = 0  # set nan for zero
    # 设定nan 为数据列的平均值
    for i in range(newData.shape[1]):
        newData[:, i][np.isnan(newData[:, i])] = np.mean(newData[:, i][~np.isnan(newData[:, i])])

    print "after fiter,shape:", newData.shape
    if typeNum == 2:

        # 过滤掉其他的数据

        rmRow = (label > -0.01) & (label < 0.01)
        rmRow = rmRow.reshape(m)
        label = label[~rmRow, :]
        newData = newData[~rmRow, :]

        ori_label = label.copy()
        # 处理label,分成两类
        label[label >= 0.01] = 1
        label[label <= -0.01] = -1

        print "data.shape,lable,shape", newData.shape, label.shape

        # 累积前五项和
        # num =range(newData.shape[0])
        # num.reverse()

        # for i in num:
        #    if(i-4>=0):
        #       newData[i,:]+=newData[i-4,:]+newData[i-3,:]+newData[i-2,:]+newData[i-1,:]


    elif typeNum == 3:
        ori_label = label.copy()
        label[label >= 0.008] = 1
        label[label <= -0.007] = -1
        label[(label > -0.007) & (label < 0.008)] = 0
    else:
        print "will to do regression"

    print "lable,len(1),len(-1),len(0)", len(label[label == 1]), len(label[label == -1]), len(label[label == 0])

    print "orlabel:", ori_label.shape

    #0-1标准化－－－－范围缩放标准化(0-1 normalization)
    # 范围缩放标准化
    min_max_scaler = preprocessing.MinMaxScaler()
    # 训练集缩放标准化
    newData=min_max_scaler.fit_transform(newData)


    # 转化label为一维数组
    return newData, label[:, 0], ori_label[:, 0]


# 数据分为两部分进行验证
def splitTrainAndTest(data, label, originalLable):
    m, n = data.shape
    test_rate = int(m * 0.7)
    # X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.3, random_state=0)
    X_train = data[0:test_rate]
    y_train = label[0:test_rate]
    X_test = data[test_rate:]
    y_test = label[test_rate:]
    originalLable = originalLable[test_rate:]

    print "acutual_training,1,-1,0:", len(y_train[y_train == 1]), len(y_train[y_train == -1]), len(
        y_train[y_train == 0])
    print "acutual_tesing,1,-1,0:", len(y_test[y_test == 1]), len(y_test[y_test == -1]), len(y_test[y_test == 0])

    return X_train, y_train, X_test, y_test, originalLable


# svm 预测
def svm_predict(X_train, y_train, X_test, y_test):
    '''
        probas_ = clf.fit(X_train, y_train).predict_proba(X_test)
        fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1],pos_label=1)
        au = auc(fpr, tpr)
        # print "predict,1,-1,0", len(predict_y[predict_y == 1]), len(predict_y[predict_y == -1]), len(
        #  predict_y[predict_y == 0])
        if (au > roc_auc):
            roc_auc = au
            r_i = i
            r_c = cc
        end_t = time.time()
        print  "result:", roc_auc, r_i, r_c, (end_t - start_t)
        '''
    cc = 10
    ga = 0.175
    clf = svm.SVC(probability=True, C=cc, kernel='rbf', gamma=ga,
                  random_state=0, decision_function_shape='ovo')
    clf.fit(X_train, y_train)
    p_y = clf.predict(X_test)
    score = clf.score(X_test, y_test)
    print 'score:', score
    return p_y


# np.hstack((a,b))
# svm 预测
def svm_predict_optimize(X_train, y_train, X_test, y_test):
    '''
        probas_ = clf.fit(X_train, y_train).predict_proba(X_test)
        fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1],pos_label=1)
        au = auc(fpr, tpr)
        # print "predict,1,-1,0", len(predict_y[predict_y == 1]), len(predict_y[predict_y == -1]), len(
        #  predict_y[predict_y == 0])
        if (au > roc_auc):
            roc_auc = au
            r_i = i
            r_c = cc
        end_t = time.time()
        print  "result:", roc_auc, r_i, r_c, (end_t - start_t)
        '''
    cc = 10
    ga = 0.175
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
        print "len,i",testNum,i

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


def plotResult(ori_y_test, y_test, y_predict,typeNum):

    print "predict_tesing,1,-1,0:", len(y_predict[y_predict == 1]), len(y_predict[y_predict == -1]), len(
        y_predict[y_predict == 0])

    # 测试效果详情
    from sklearn import metrics
    print(metrics.classification_report(y_test, y_predict))
    print metrics.confusion_matrix(y_test, y_predict)

    testNum = y_predict.size

    net_value = np.zeros((testNum, 4))
    # 计算累积单位净值
    pp = y_predict[y_test == y_predict]
    up = len(pp[pp == 1])  # 做多次数
    down = len(pp[pp == -1])  # 做空次数
    print "做多up次数,做空down次数", up, down
    net_up = 1.0  # 做多
    net_down = 1.0  # 做空
    net_all = 1.0  # 都做
    net_ori = 1.0  # 原始基线

    for i in range(testNum):
        # 只做多
        if (y_predict[i] == 1):
            net_up = net_up * (1 + ori_y_test[i])
        elif (y_predict[i] == -1):
            net_down = net_down * (1 - ori_y_test[i])

        net_all = net_all * (1 + y_predict[i] * ori_y_test[i])
        net_ori = net_ori * (1 + ori_y_test[i])

        net_value[i, 0] = net_up
        net_value[i, 1] = net_down
        net_value[i, 2] = net_all
        net_value[i, 3] = net_ori

    plt.plot(range(0, testNum), net_value[:, 0], linestyle='-', lw=2, color='k',
             label='only_go_long')
    plt.plot(range(0, testNum), net_value[:, 1], linestyle='-', lw=2, color='b',
             label='only_go_short')
    plt.plot(range(0, testNum), net_value[:, 2], linestyle='-', lw=2, color='y',
             label='short_long_all')
    plt.plot(range(0, testNum), net_value[:, 3], linestyle='-', lw=2, color='r',
             label='base')

    from matplotlib.font_manager import FontProperties
    f = FontProperties(fname="/System/Library/Fonts/STHeiti Light.ttc", size=10)

    plt.xlabel(u'时间',fontproperties=f)
    plt.ylabel('net')
    plt.title(str(typeNum) +' classes-accumulative net value')
    plt.legend(loc=2)
    plt.show()


def select_model_predict(X_train, y_train, X_test, y_test, model='svm'):
    if (model == 'svm'):
        return svm_predict(X_train, y_train, X_test, y_test)
    elif (model == 'ada'):
        return adaboost_predict(X_train, y_train, X_test, y_test)
    elif (model=='svm_opt'):
        return svm_predict_optimize(X_train, y_train, X_test, y_test)
    print "ERROR type for ", model


# 降维，降到15维度
def pca_reduce_demension(data):
    pca = PCA()
    pca.fit(data)


    plt.figure(1, figsize=(4, 3))
    plt.clf()
    plt.axes([.2, .2, .7, .7])
    plt.plot(pca.explained_variance_, linewidth=2)
    plt.axis('tight')
    plt.xlabel('n_components')
    plt.ylabel('explained_variance_')
    plt.show()

    data = pca.fit_transform(data)
    return data


def plotOriTrend(ori_label,label):
    testNum = ori_label.shape[0]
    net_value = np.zeros((testNum,3))
    net_ori = 1.0  # 原始基线
    for i in range(testNum):
        net_ori = net_ori * (1 + ori_label[i])
        net_value[i,0] = net_ori
        net_value[i,1] = ori_label[i]
        net_value[i,2] = label[i]

    plt.plot(range(0, testNum), net_value[:,0], linestyle='-', lw=2, color='k',
             label='net_acc_ori')
    plt.plot(range(0, testNum), net_value[:,1], linestyle='-', lw=2, color='y',
             label='net_base_ori')
    plt.plot(range(0, testNum), net_value[:,2], linestyle='-', lw=2, color='r',
             label='net_label')

    plt.xlabel('time')
    plt.ylabel('ori_net')
    plt.title('ori data statistics')
    plt.legend(loc=2)
    plt.show()


def main():
    classNum=3
    # 加载数据
    dateList, data, label = loadData()
    # 过滤数据
    data, label, ori_label = filterData(data, label, classNum)
    # plot
    #plotOriTrend(ori_label,label)
    # 降低维度
    #data=pca_reduce_demension(data)
    # 分割训练数据集和测试数据集
    X_train, y_train, X_test, y_test, ori_label = splitTrainAndTest(data, label, ori_label)
    # 计算模型和预测结果
    predict_y = select_model_predict(X_train, y_train, X_test, y_test, 'svm') #svm or ada
    # 画图
    plotResult(ori_label, y_test, predict_y,classNum)


main()
