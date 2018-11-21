# -*- coding=utf8 -*-
'''
import matplotlib as mpl


import matplotlib.pyplot as plt


from matplotlib.font_manager import FontProperties

print mpl.matplotlib_fname()


if __name__ == "__main__":

    mpl.rcParams['axes.unicode_minus'] = False
    font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')
    plt.figure()
    plt.title(u'中文测试', fontsize=18, fontproperties=font);
    plt.xlabel(u'横轴',fontproperties=font)
    plt.ylabel(u'纵轴',fontproperties=font)
    plt.show()

'''

import matplotlib
import matplotlib.pyplot as pl
matplotlib.use('qt4agg')
#指定默认字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
#解决负号'-'显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False
pl.plot([-1,2,-5,3])
pl.title(u'中文')
pl.show()


