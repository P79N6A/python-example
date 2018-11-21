# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
import kpi_index as kpi
import talib as ta

# dataFrame
df = pd.read_csv('./hb_data_30min.csv', sep=',', index_col=0)

count_display=300

#df=df.iloc[-count_display:]

def plot_picture(df):
    kdj = kpi.get_kdj(df)
    macd = kpi.get_macd(df)
    ma = kpi.get_ma(df, 4,5,10, 37, 114)

    fig= plt.figure(1)
    #plt.vlines(100, -1000, 1000, colors="k", linestyles="dashed")

    ax1=plt.subplot(411)
    plt.plot(df['close'].values,label='close')
    plt.plot(ma['5ma'].values, 'r-', label='5ma')
    plt.legend()

    ax2= plt.subplot(412)
    plt.plot(kdj['K'].values,'r-',label='k')
    plt.plot(kdj['D'].values,label='d')
    plt.plot(kdj['J'].values,label='j')
    plt.hlines(100, 0, count_display, colors="k", linestyles="dashed")
    plt.hlines(0, 0, count_display, colors="k", linestyles="dashed")
    plt.legend()

    ax3=plt.subplot(413)
    #macd.plot()
    plt.plot(macd['DIF'].values, 'r-', label='DIF')
    plt.plot(macd['DEA'].values, label='DEA')
    #plt.plot(macd['MACD'].values, label='MACD')
    n, bins, patches = plt.hist(macd['MACD'].values, bins=count_display, normed=1, facecolor='green', alpha=0.75)
    plt.hlines(0, 0, count_display, colors="k", linestyles="dashed")
    plt.legend()


    ax4=plt.subplot(414)
    #plt.plot(ma['5ma'].values, 'r-', label='5ma')
    #plt.plot(ma['10ma'].values, label='10ma')
    plt.plot(ma['37ma'].values, label='37ma')
    plt.plot(ma['114ma'].values, label='114ma')
    #ma.plot()
    plt.legend()

    multi = MultiCursor(fig.canvas, (ax1, ax2,ax3,ax4), color='r', lw=1)
    plt.show()

plot_picture(df)
# macd_tmp=ta.MACD(df['close'].values)
# DIF = macd_tmp[0]
# DEA = macd_tmp[1]
# MACD = macd_tmp[2]

def kd(df):
    min = df.iloc[:, 3].min()
    max = df.iloc[:, 3].max()

    # kdj
    kdj_df = kpi.get_kdj(df, days=30)
    macd_df = kpi.get_macd(df)


    profit_df = pd.DataFrame(index=range(2000), columns=['acc_net'])
    acc_net = 1
    ltc = 0
    switch = 0
    buy_price = 0
    print "size:", profit_df.index.size

    for j in range(df.index.size):
        # 在j日操作
        i = j - 1
        if (i > 10):
            #
            if ((kdj_df.iloc[i - 1, 0] < kdj_df.iloc[i - 1, 1])  # k昨日 < D 昨日
                and (kdj_df.iloc[i, 0] > kdj_df.iloc[i, 1])  # k今日 > D 今日
                and (macd_df.iloc[i, 2] > macd_df.iloc[i - 1, 2])  # MACD今日>MACD 昨日
                and macd_df.iloc[i, 2] < 0
                and macd_df.iloc[i - 1, 2] < 0
                and (kdj_df.iloc[i - 1, 2] < 0 or kdj_df.iloc[i - 2, 2] < 0 or kdj_df.iloc[i, 2] < 0)
                and switch == 0):  # buy
                switch = 1
                ltc = acc_net * 1.0 / df.iloc[j, 3] * 0.998
                buy_price = df.iloc[j, 3]
                print 'buy', switch, df.index[j], df.iloc[j, 3]
                plt.vlines(j, min, max, colors="k", linestyles="dashed")

            elif ((kdj_df.iloc[i - 1, 0] > kdj_df.iloc[i - 1, 1])  # k昨日 > D 昨日
                  and (kdj_df.iloc[i, 0] < kdj_df.iloc[i, 1])  # k今日 <D 今日
                  and (macd_df.iloc[i, 2] < macd_df.iloc[i - 1, 2])  # MACD今日<MACD 昨日
                  and macd_df.iloc[i, 2] > 0
                  and macd_df.iloc[i - 1, 2] > 0
                  and switch == 1
                  and (kdj_df.iloc[i - 1, 2] > 100 or kdj_df.iloc[i - 2, 2] > 100 or kdj_df.iloc[i, 2] > 100)
                  and df.iloc[j, 3] >= buy_price):  # bsell
                switch = 0
                acc_net = ltc * df.iloc[j, 3] * 0.998
                print 'sell', switch, df.index[j], df.iloc[j, 3]
                plt.vlines(j, min, max, colors='r', linestyles="dashed")

        profit_df.iloc[j, 0] = acc_net

    plt.plot(df['close'].values, label='close')
    plt.legend()
    plt.show()

    print 'acc', acc_net
    profit_df.plot()
    plt.show()


# ＝＝＝＝＝＝判断趋势＝＝＝＝＝＝＝＝＝＝
# 如果是上升趋势
# 如果是下降趋势
# 如果是横盘


def kd_macd(df):
    min = df.iloc[:, 3].min()
    max = df.iloc[:, 3].max()

    # kdj
    kdj_df = kpi.get_kdj(df, days=30)
    # macd
    macd_df = kpi.get_macd(df, short=30, long=60)

    profit_df = pd.DataFrame(index=range(2000), columns=['acc_net'])
    acc_net = 1
    ltc = 0
    switch = 0
    buy_price = 0
    print "size:", profit_df.index.size

    for j in range(df.index.size):
        # 在j日操作
        i = j - 1
        if (i > 10):
            #
            if ((kdj_df.iloc[i - 1, 0] < kdj_df.iloc[i - 1, 1])  # k昨日 < D 昨日
                and (kdj_df.iloc[i, 0] > kdj_df.iloc[i, 1])  # k今日 > D 今日
                and (macd_df.iloc[i, 2] > macd_df.iloc[i - 1, 2])  # MACD今日>MACD 昨日
                and macd_df.iloc[i, 2] < 0
                and macd_df.iloc[i - 1, 2] < 0
                and (kdj_df.iloc[i - 1, 2] < 0 or kdj_df.iloc[i - 2, 2] < 0 or kdj_df.iloc[i, 2] < 0)
                and switch == 0):  # buy
                switch = 1
                ltc = acc_net * 1.0 / df.iloc[j, 3] * 0.998
                buy_price = df.iloc[j, 3]
                print 'buy', switch, df.index[j], df.iloc[j, 3]
                plt.vlines(j, min, max, colors="k", linestyles="dashed")

            elif ((kdj_df.iloc[i - 1, 0] > kdj_df.iloc[i - 1, 1])  # k昨日 > D 昨日
                  and (kdj_df.iloc[i, 0] < kdj_df.iloc[i, 1])  # k今日 <D 今日
                  and (macd_df.iloc[i, 2] < macd_df.iloc[i - 1, 2])  # MACD今日<MACD 昨日
                  and macd_df.iloc[i, 2] > 0
                  and macd_df.iloc[i - 1, 2] > 0
                  and switch == 1
                  and (kdj_df.iloc[i - 1, 2] > 100 or kdj_df.iloc[i - 2, 2] > 100 or kdj_df.iloc[i, 2] > 100)
                  and df.iloc[j, 3] >= buy_price):  # bsell
                switch = 0
                acc_net = ltc * df.iloc[j, 3] * 0.998
                print 'sell', switch, df.index[j], df.iloc[j, 3]
                plt.vlines(j, min, max, colors='r', linestyles="dashed")

        profit_df.iloc[j, 0] = acc_net

    plt.plot(df['close'].values, label='close')
    plt.legend()
    plt.show()

    print 'acc', acc_net
    profit_df.plot()
    plt.show()

def j_macd(df):
    min = df.iloc[:, 3].min()
    max = df.iloc[:, 3].max()

    # kdj
    kdj_df = kpi.get_kdj(df, days=30)
    # macd
    macd_df = kpi.get_macd(df, short=30, long=60)

    profit_df = pd.DataFrame(index=range(2000), columns=['acc_net'])
    acc_net = 1
    ltc = 0
    switch = 0
    buy_price = 0
    print "size:", profit_df.index.size

    for j in range(df.index.size):
        # 在j日操作
        i = j - 1
        if (i > 10):
            #
            if ((kdj_df.iloc[i, 2] < 0 or  kdj_df.iloc[i - 1, 2]<0 or  kdj_df.iloc[i - 2, 2]<0)  # j昨日 or  j今日 < 0
                and macd_df.iloc[i, 2]>0
                and switch == 0):  # buy
                switch = 1
                ltc = acc_net * 1.0 / df.iloc[j, 3] * 0.998
                buy_price = df.iloc[j, 3]
                print 'buy', switch, df.index[j], df.iloc[j, 3]
                plt.vlines(j, min, max, colors="k", linestyles="dashed")

            elif ((kdj_df.iloc[i - 1, 2] >100 or  kdj_df.iloc[i , 2]>100 or  kdj_df.iloc[i-2 , 2]>100)  # j昨日 or  j今日 >100
                  and switch == 1):  # bsell
                switch = 0
                acc_net = ltc * df.iloc[j, 3] * 0.998
                print 'sell', switch, df.index[j], df.iloc[j, 3]
                plt.vlines(j, min, max, colors='r', linestyles="dashed")

        profit_df.iloc[j, 0] = acc_net

    plt.plot(df['close'].values, label='close')
    plt.legend()
    plt.show()

    print 'acc', acc_net
    profit_df.plot()
    plt.show()

def ma_both(df,m_short,m_long,v_short,v_long,enable_m=True,enable_v=True,plot=False):
    #alpaha
    alpha=1
    # ma
    ma_df = kpi.get_ma(df, 3, m_short, m_long)
    v_df = kpi.get_ma(df, 4, v_short, v_long)
    min = df.iloc[:, 3].min()
    max = df.iloc[:, 3].max()
    profit_df = pd.DataFrame(index=range(2000), columns=['acc_net'])
    acc_net = 1
    ltc = 0
    switch = 0
    buy_price = 0
    print "size:", profit_df.index.size

    fast_ma = 0 #short
    slow_ma = 1 #long

    right_c=0
    false_c=0

    if(plot):
        plt.subplot(3, 1, 1)

    for j in range(df.index.size):
        i = j - 1
        if (i > m_long and i> v_long):

            buy_a=False
            if(enable_m and enable_v):
                buy_a=can_buy(ma_df, i, fast_ma, slow_ma, switch) or can_buy(v_df, i, fast_ma, slow_ma, switch)
            elif(enable_m):
                buy_a = can_buy(ma_df, i, fast_ma, slow_ma, switch)
            else:
                buy_a = can_buy(v_df, i, fast_ma, slow_ma, switch)

            sell_a=False
            if (enable_m and enable_v):
                sell_a = can_sell(ma_df, i, fast_ma, slow_ma, switch) or can_sell(v_df, i, fast_ma, slow_ma, switch)
            elif (enable_m):
                sell_a = can_sell(ma_df, i, fast_ma, slow_ma, switch)
            else:
                sell_a = can_sell(v_df, i, fast_ma, slow_ma, switch)

            if ( buy_a ):
                switch = 1
                ltc = round(acc_net   * 1.0 / df.iloc[j, 3] * 0.998,4)
                buy_price = df.iloc[j, 3]
                print 'buy', switch, df.index[j], df.iloc[j, 3],alpha,ltc
                if (plot):
                    plt.vlines(j, min, max, colors="k", linestyles="dashed")

            elif(sell_a and abs(df.iloc[j, 3]-buy_price)>1.0):
                switch = 0
                acc_net = ltc * df.iloc[j, 3] * 0.998
                right=True if df.iloc[j, 3]>buy_price else False
                if(right):
                    right_c+=1
                else:
                    false_c+=1
                print 'sell', switch, df.index[j], df.iloc[j, 3],right,acc_net
                if (plot):
                    plt.vlines(j, min, max, colors='r', linestyles="dashed")
            profit_df.iloc[j, 0] = acc_net


    if(right_c+false_c==0):
        print 'acc 1'
    else:
        print 'acc:',acc_net,right_c,false_c,(right_c+false_c),(right_c*1.0/(right_c+false_c))

    if (plot):

        plt.plot(df['close'].values, label='close')
        plt.legend()
        plt.subplot(3, 1, 2)
        plt.plot(v_df.iloc[:, fast_ma].values, label='short_ma')
        plt.plot(v_df.iloc[:, slow_ma].values, label='long_ma')
        plt.legend()
        plt.subplot(3, 1, 3)
        plt.plot(profit_df.values, label='acc')
        plt.legend()

        plt.show()

    return acc_net



def can_buy(ma_df, i, fast_ma, slow_ma, switch):
    return (ma_df.iloc[i - 1, fast_ma] < ma_df.iloc[i - 1, slow_ma]
            and ma_df.iloc[i, fast_ma] >= ma_df.iloc[i, slow_ma]
            and switch == 0)


def can_sell(ma_df, i, fast_ma, slow_ma, switch):
    return (ma_df.iloc[i - 1, fast_ma] > ma_df.iloc[i - 1, slow_ma]
            and ma_df.iloc[i, fast_ma] <= ma_df.iloc[i, slow_ma]
            and switch == 1)



def ma_for(df):
    slow=[20,25,30,35,40,50,60]
    fast=[60,80,85,90,100,120,240]

    #slow = np.arange(35,40,1)
    #fast=np.arange(95,115,1)
    max_acc=0,
    max_slow=20
    max_fast=60
    for s in slow:
        for f in fast:
            print s,f
            acc=ma_both(df,20,90,s,f,False,True)
            if(acc>max_acc):
                max_acc=acc
                max_slow=s
                max_fast=f

            print 'max acc:',max_acc
            print max_slow, max_fast



#ma(df,35,100) #20,90,73.8
#ma_for(df)
ma_both(df,20,90,37,114,True,True,True)

# kdj_macd(df)
#j_macd(df)

#20,240 对应5分钟
#20,90 对应1分钟 ,在上涨趋势中表现好