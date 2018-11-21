
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np



fig = plt.figure()
ax0=fig.add_subplot(1,1,1)
ax0.plot(np.arange(1,10,1),'gs-')
#fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
fig.show()
#概率分布直方图
#高斯分布
#均值为0
mean = 0
#标准差为1，反应数据集中还是分散的值
sigma = 1
x=mean+sigma*np.random.randn(40)
print x

fig,(ax0,ax1) = plt.subplots(nrows=2,figsize=(9,6))
#第二个参数是柱子宽一些还是窄一些，越大越窄越密
ax0.hist(x,40,normed=1,histtype='bar',facecolor='yellowgreen',alpha=0.75)
##pdf概率分布图，一万个数落在某个区间内的数有多少个
ax0.set_title('pdf')
ax1.hist(x,20,normed=1,histtype='bar',facecolor='pink',alpha=0.75,cumulative=True,rwidth=0.8)
#cdf累计概率函数，cumulative累计。比如需要统计小于5的数的概率
ax1.set_title("cdf")
fig.subplots_adjust(hspace=0.4)
plt.show()