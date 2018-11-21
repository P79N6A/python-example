# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor

import numpy as np
import time
from time import sleep

class MethodCount:
    def loadDataSet(self,fileName):
        dataList = [];
        fr = open(fileName,'r')
        for line in fr.readlines():
            item = line.strip();
            dataList.append(float(item));

        self.dataMat= np.array(dataList);
        self.dataMat=self.dataMat.cumsum();
        print self.dataMat

    def figure(self):
        # 创建一个的图，并设置分辨率为 80
        fig=plt.figure()  # 可以省略
        # 创建一个新的 1 * 1 的子图，接下来的图样绘制在其中的第 1 块（也是唯一的一块）
        ax=plt.subplot(1, 1, 1) ; # 如果只有一个图则省略即可
        plt.plot(self.dataMat);
        # 另外一种表达式方式是
        plt.plot(np.arange(self.dataMat.size), self.dataMat, 'rs-', linewidth=0.5)
        # 设置横轴的上下限
        plt.xlim(0, 104)
        # 设置横轴记号
        #plt.xticks(np.linspace(0, 104, 105, endpoint=True))
        # 设置纵轴的上下限
        plt.ylim(30, 100)
        # 设置纵轴记号
        #plt.yticks(np.linspace(30, 100, 71, endpoint=True))
        # 以分辨率 72 来保存图片
        #plt.savefig("zhoupj.png", dpi=72)

        plt.xlabel(u'method count');
        plt.ylabel('use rate')

        # 显示图示
        plt.legend()

        multi = MultiCursor(fig.canvas, [ax], color='g',horizOn=True,vertOn=True,lw=1)
        plt.show()
        # 在屏幕上显示
        plt.show()


if __name__ == '__main__':
    df = MethodCount();
    df.loadDataSet('method_invoke_rate.txt');
    df.figure();