# -*- coding:utf-8 -*-


'''
Created on 20170709
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# df pandas.DataFrame,columns='open,high,low,close,volume....'
# 顺序必须符合上述要求
# 计算kdj
def get_kdj(df, days=9, m1= 3, m2= 3,high_idx=1,low_idx=2,close_idx=3):
    kdj = pd.DataFrame(index=range(df.index.size), columns=['K', 'D', 'J'])
    print len(df.values)
    for i in range(len(df.values)):
        if i - days < 0:
            b = 0
        else:
            b = i - days + 1
        block_df = df.iloc[b:i + 1, 0:5]
        RSV = ((block_df.iloc[-1, close_idx] - block_df.iloc[:, low_idx].min()) * 1.0 / (block_df.iloc[:, high_idx].max() - block_df.iloc[:, low_idx].min())) * 100
        if i==0:
            K=RSV
            D=RSV
        else:
            K = 1.0/m1 * RSV+(m1-1)*1.0/m1 * K
            D =  1.0/m2 * K+ (m2-1)*1.0/m2 * D
        J = 3 * K - 2 * D
        kdj.iloc[i, 0] = K
        kdj.iloc[i, 1] = D
        kdj.iloc[i, 2] = J
    print kdj
    return kdj

# 计算macd
def get_macd(df, short=12,long=26,m=9,close_idx=3):
    print len(df.values)
    macd_df = pd.DataFrame(index=range(df.index.size), columns=['DIF', 'DEA', 'MACD'])
    a=count_EMA(df,short,close_idx)
    b=count_EMA(df,long,close_idx)
    #dif
    macd_df.loc[:,'DIF']=a-b
    #dea
    for i in range(macd_df.index.size):
        if(i==0):
            macd_df.iloc[i, 1] = macd_df.iloc[i, 0]
        else:
            macd_df.iloc[i,1]= (2 * macd_df.iloc[i,0] + (m - 1) * macd_df.iloc[i-1, 1]) / (m + 1)
    #macd
    macd_df.iloc[:,2]=2*(macd_df.iloc[:,0]-macd_df.iloc[:,1])
    print macd_df
    return macd_df

def count_EMA(df,N,close_idx):
    ema=np.zeros((df.index.size))
    for i in range(len(df)):
        if i==0:
            ema[i]=df.iloc[i,close_idx]
        if i>0:
            ema[i]=(2*df.iloc[i,close_idx]+(N-1)*ema[i-1])/(N+1)
    return ema

#计算均线
def get_ma(df,close_idx=3,*args):
    #print args
    ma_df = pd.DataFrame(index=range(df.index.size), columns=[str(item)+'ma' for item in args])

    for index,ct in enumerate(args):
        for i in range(df.index.size):
            start= (i+1-ct if i+1>ct else 0)
            end=i+1
            ma_df.iloc[i,index]=df.iloc[start:end,close_idx].mean()
    #print ma_df
    return ma_df


if __name__ == '__main__':
    df = pd.DataFrame(data=np.random.randint(30,100, size=(100, 5)), columns=['open', 'high', 'low', 'close', 'volume'])
    df.loc[:,'high']=  df.loc[:,'close']+3
    df.loc[:, 'low'] = df.loc[:, 'close'] - 1
    print df
    #kdj = get_kdj(df)
    macd=get_ma(df,3,5,30)
    macd.plot()
    plt.show()


