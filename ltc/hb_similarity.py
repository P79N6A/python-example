# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import thread
import threading



def load_data():
    # dataFrame
    df = pd.read_csv('./hb_data_H.csv', sep=',',index_col=0)
    #df.set_index(['time'], inplace=True)
    #dti=pd.date_range('2017.02.01', periods=7, freq='D')
    #pydate_array = dti.to_pydatetime()
    #date_only_array = np.vectorize(lambda s: s.strftime('%Y.%m.%d'))(pydate_array)
    #date_only_series = pd.Series(date_only_array)
    return df

#数据转化为：0-23 小时为 index,日期为columns,0小时很多数据没有，填充为1小时的
def filter_data(df):
    # dataFrame
    df = df.loc[:, ['time', 'CLOSE']]
    df = df.reset_index()
    df.set_index(['date', 'time'], inplace=True)
    df = df.unstack(level=0)

    # 最后1列数据删除和第一列数据删除
    df=df.iloc[:,1:-1]
    # 对nan值进行处理
    df=df.fillna(method='pad')
    df = df.fillna(method='bfill')
    print df.shape
    return df


# 历史数据天数 his_days
# 相关系数阈值 coefficent_threshold
# his_days有多少天的比例是符合上述阈值要求的 data_rate_threshold
# 如果最高价和最低价的差价比率超过diff_trade，则进行交易 diff_trade
def find_best_parameter(df,his_days = 5,coefficent_threshold = 0.8,data_rate_threshold = 0.7,diff_trade_rate=0.003,c='k'):

    trade_num=0
    net_list=np.ones((df.shape[1]))
    net_acc=1.0
    for days in range(df.shape[1]):

        if(days+his_days<df.shape[1]):
            once_df=df.iloc[:,days:days+his_days]
            similar_map=find_similar_point_with_steps(once_df,coefficent_threshold,data_rate_threshold)
            #print similar_map
            trade_list=find_trade_point_with_best_steps(once_df,similar_map,diff_trade_rate)
            #print trade_list
            test_df=df.iloc[:,days+his_days]
            print "day:", (days + his_days),
            for tu in trade_list:
                trade_num+=1
                #print  'step:',tu[3]
                if(tu[0]=='s'):
                    net_acc=net_acc*(1+ (test_df[tu[1]]-test_df[tu[2]])/test_df[tu[1]])
                else:
                    net_acc = net_acc/test_df[tu[1]]*0.998*test_df[tu[2]]*0.0998
            print net_acc
            net_list[days+his_days]  = net_acc

    #print net_list
    plt.plot(range(df.shape[1]), net_list, linestyle='-', lw=2, color=c, label='his_days='+str(his_days))
    print 'trade count:',trade_num
    return trade_num


#找到波动相似的点和数据
def find_similar_point_with_steps(df ,coefficent_threshold ,data_rate_threshold):

    rst_map={2:[],3:[],4:[],5:[],6:[]}
    max_rate = 0.0
    min = df.values.min()
    max = df.values.max()
    #df.plot()
    for step in rst_map.keys():
        for h in range(df.shape[0]):
            if (h + step <= df.shape[0]):
                # print 'continue,h',h,h+step
                dff = df.iloc[h:h + step, :]
                dfcorr = dff.corr()  # 计算相关系数
                for row in range(dfcorr.shape[0]):  # 遍历看那一组是符合要求的
                    coefficent_threshold_num = dfcorr.iloc[row][dfcorr.iloc[row] >= coefficent_threshold].size
                    # print coefficent_threshold_num,dfcorr.shape[1]
                    rate = coefficent_threshold_num * 1.0 / dfcorr.shape[1]
                    if (rate >= data_rate_threshold):
                        # plt.vlines(h, min, max, colors="c", linestyles="dashed")
                        # plt.vlines(h + step - 1, min, max, colors='k', linestyles="dashed")
                        #print dfcorr.index.values[row][1], h,'-',h + step - 1, rate,step
                        #rst.append((row, h, h + step - 1,step))
                        rst_map.get(step).append((row, h, h + step - 1,step))
                        break

   # plt.legend(loc=2)
   # plt.xlim(0, 24)
   # plt.show()
    return rst_map

#找到可以交易的点，现在只考虑单调曲线情况，先买后卖
def find_trade_point_with_best_steps(once_df,rst_map,diff_trade_rate):
    rst=find_best_step_on_hisday(once_df,rst_map)
    trade_list=[]
    for tu in rst:
        start=once_df.iloc[tu[1],tu[0]]
        end=once_df.iloc[tu[2],tu[0]]
        if((end-start)/start>=diff_trade_rate):#做多
            print 'buy in', tu[1], 'end in', tu[2],'date:',tu[0],'step:',tu[3]
            trade_list.append(('b',tu[1], tu[2],tu[3]))
    return trade_list


def find_best_step_on_hisday(once_df,rst_map):
    max=-1000000.0
    best_step=0
    for step in rst_map.keys():
        s=0.0
        for tu in rst_map.get(step):
            start = once_df.iloc[tu[1], tu[0]]
            end = once_df.iloc[tu[2], tu[0]]
            if (start < end ):  # 做多
                s = s + (once_df.iloc[tu[2], :] - once_df.iloc[tu[1], :]).mean()
        #print 'step,s',step,s
        if(s>max):
            max=s
            best_step=step

    return rst_map.get(best_step)




class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, df,his_day,color,thread_name):
        threading.Thread.__init__(self)
        self.name = thread_name
        self.df = df
        self.color=color
        self.his_day=his_day

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting " + self.name
        num=find_best_parameter(self.df,his_days=self.his_day, c=self.color)
        print "Exiting " + self.name,num




#r 红 g 绿 b 蓝 c 蓝绿 m 紫红 y 黄 k 黑 w 白
def plot_step(df):
    color=['r','g','b','c','m','y','k','w']
    his_days=[7,10,11,12,13]
    threads=[]
    for idx,dy in enumerate(his_days):
        thr=myThread(df,dy,color[idx],'thread-'+str(idx))
        thr.start()
        threads.append(thr)

    for t in threads:
        t.join()
    print 'over'
    plt.xlabel('time')
    plt.ylabel('net')
    plt.title('net data statistics')
    plt.legend(loc=2)
    plt.show()

def main():
    #黄金数据
    #file='./XAUUSD.csv'
    # 运行一边后，下一行代码可以注释掉
    #process_data_from_minute_to_hour(file)
    df=load_data()
    df=filter_data(df)
    print df
    #df=df.iloc[:,-1000:]
    #plot_step(df)


main()
