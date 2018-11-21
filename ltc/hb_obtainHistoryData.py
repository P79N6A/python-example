# encoding: utf-8

from vnhuobi import *
import pandas as pd
import matplotlib.pyplot as plt
import kpi_index as kpi
import threading
import time


# ----------------------------------------------------------------------
def trade():
    """测试交易"""
    accessKey = '6d00f5fc-f9b751c7-304c7db8-9cb02'
    secretKey = 'da858b5a-25694648-87b30050-5b3e0'

    # 创建API对象并初始化
    api = TradeApi()
    api.DEBUG = True
    api.init(accessKey, secretKey)

    # 查询账户，测试通过
    # api.getAccountInfo()

    # 查询委托，测试通过
    # api.getOrders(coinType=COINTYPE_LTC)

    # 买入，测试通过
    # api.buy(7100, 0.0095)

    # 卖出，测试通过
    # api.sell(7120, 0.0095)

    # 撤单，测试通过
    # api.cancelOrder(3915047376L)

    # 查询杠杆额度，测试通过
    # api.getLoanAvailable()

    # 查询杠杆列表，测试通过
    # api.getLoans()

    # 阻塞
    # input()
    api.exit()


# ----------------------------------------------------------------------
def histData():
    """测试行情接口"""
    api = DataApi()
    api.init(0.5, False)
    # 订阅成交推送，测试通过
    # api.subscribeTick(SYMBOL_BTCCNY)
    # 订阅报价推送，测试通过
    # api.subscribeQuote(SYMBOL_BTCCNY)
    # 订阅深度推送，测试通过
    # api.subscribeDepth(SYMBOL_BTCCNY, 1)
    # 查询K线数据，测试通过

    data = api.getKline(SYMBOL_LTCCNY, PERIOD_1MIN, 2000)
    df = pd.DataFrame(data=data, columns=['time', 'open', "high", "low", "close", "volume"])
    print df.iloc[-1, 0]
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print now


    print len(data)

    print df
    # df=df.set_index(keys=["time"])
    # df['date']=[ x[0:8] for x in df.loc[:,'time'].values]
    # df.loc[:,'time']=[ x[8:10] for x in df.loc[:,'time'].values]
    # df=df.loc[:,['date','time','OPEN',"HIGH","LOW","CLOSE","VOLUME"]]
    df.to_csv('./hb_data_1min.csv', sep=',', index=False)
    # kpi_df=kpi.get_kdj(df,high_idx=2,low_idx=3,close_idx=4)
    # kpi_df.plot()
    # plt.show()

    api.exit()  # if __name__ == '__main__':

#trade()
histData()
