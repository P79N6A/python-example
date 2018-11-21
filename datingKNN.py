import operator
from numpy import *
import matplotlib.pyplot as plt


# read file
def file2matrix(filename):
    fr = open(filename)
    arrayolines = fr.readlines()
    num = len(arrayolines)
    returnmat = zeros((num, 3))
    vectors = []
    index = 0
    for line in arrayolines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnmat[index, :] = listFromLine[0:3]
        vectors.append(int(listFromLine[-1]))
        index += -1
    return returnmat, vectors


# 数据归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))  # element wise divide
    return normDataSet, ranges, minVals


def run(mat, labes):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    lab = set(labes)
    color = {}
    color[1] = 'r'
    color[2] = 'g'
    color[3] = 'm'
    for item in lab:
        print item
        # mat[:,3]
        ind = squeeze(asarray(labes)) == item  # 筛选条件
        # print ind
        matt = mat[ind, :]
        ax.scatter(matt[:, 1], matt[:, 2], s=15.0 * item, c=color[item], label=item)
    plt.title('Scatter')
    plt.xlabel('play game')
    plt.ylabel('eat ')
    plt.grid(True)
    plt.legend()
    plt.show()


def main(filename):
    mat, labes = file2matrix(filename)
    normDataSet, ranges, minVals = autoNorm(mat)
    run(normDataSet, labes)


main('dating.txt')
