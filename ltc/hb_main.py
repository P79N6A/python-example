# encoding: utf-8

from vnhuobi_sync import *
import pandas as pd
import kpi_index as kpi
import threading
import time
import sys


#----------------------------------------------------------------------
def trade_init():
    """测试交易"""
    accessKey = '6d00f5fc-f9b751c7-304c7db8-9cb02'
    secretKey = 'da858b5a-25694648-87b30050-5b3e0'
    # 创建API对象并初始化
    api = TradeApi()
    api.DEBUG = True
    api.init(accessKey, secretKey)

    return api;
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
    # api.exit()


# ----------------------------------------------------------------------
def query_and_trade(fileout):


    # 需要读取历史数据
    his_count = 120

    # 交易接口
    trade_api = trade_init();


    #result= trade_api.getNewDealOrders()
    #print 'reuslt',result


    # 查询当前是否已经买入
    switch = 0

    acc_net = 0
    ltc = 0

    # 如果当前有订单，则取消
    orders = trade_api.getOrders(coinType=COINTYPE_LTC)
    print 'order', orders;

    if (len(orders) > 0):
        for item in orders:
            id = item['id']
            cancle = trade_api.cancelOrder(id, coinType=COINTYPE_LTC)
            print cancle

    data = trade_api.getAccountInfo()
    print 'data:', data
    available_ltc_display = data['available_ltc_display']
    frozen_ltc_display = data['frozen_ltc_display']
    frozen_cny_display = data['frozen_cny_display']
    available_cny_display = data['available_cny_display']

    # 当前可用的
    ltc = available_ltc_display
    print 'ltc',ltc
    acc_net = available_cny_display

    if (float(ltc) > 0.001):  # 已经买入
        print 'start',switch
        switch = 1

    """测试行情接口"""
    his_api = DataApi()
    his_api.init(0.5, False)

    # 当前时间
    his_time = None

    # 循环访问
    while True:

        last_trade_success = True #上次交易是否成功
        cancel_order_success=True
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print 'now:',now
        # 如果当前有订单，说明之前的买入卖出的委托不成功,取消重新算
        orders = trade_api.getOrders(coinType=COINTYPE_LTC)
        if (len(orders) > 0):
            last_trade_success = False #有订单说明前一次交易未成功
            cancel_order_success=False
            print 'orders:',orders
            for item in orders:
                id = item['id']
                type = item['type']
                cancle = trade_api.cancelOrder(id, coinType=COINTYPE_LTC)
                print 'cancle',cancle
                if (cancle['ok']):
                    cancel_order_success = True
                    if (type == 1 and switch == 1):  # 有买入的订单，但是未成功，所以更新swich为0
                        switch = 0
                    elif (type == 2 and switch == 0):  # 有卖出的订单，但是未成功，所以更新swich为1
                        switch = 1



        # 得到账户信息
        data = trade_api.getAccountInfo()
        available_ltc_display = data['available_ltc_display']
        frozen_ltc_display = data['frozen_ltc_display']
        frozen_cny_display = data['frozen_cny_display']
        available_cny_display = data['available_cny_display']
        ltc = available_ltc_display;
        acc_net = float(available_cny_display)*0.99
        print 'available_ltc,available_cny,frozen_ltc,frozen_cny', ltc,available_cny_display,frozen_ltc_display,frozen_cny_display
        print 'available_cny_display*0.98', acc_net


        if (last_trade_success):  # 没有订单才可以继续处理
            print 'count if buy or sell,switch',switch
            data = his_api.getKline(SYMBOL_LTCCNY, PERIOD_30MIN, his_count)
            df = pd.DataFrame(data=data, columns=['time', 'open', "high", "low", "close", "volume"])
            if (his_time == None or his_time != df.iloc[-1, 0]):
                his_time = df.iloc[-1, 0] #下一次半个小时才需要处理，否则不需要处理
                switch = buy_or_sell(his_api, trade_api, df, switch, acc_net, ltc, now)
        elif (cancel_order_success):
            #上一次未成功交易，重新交易
            data = his_api.getKline(SYMBOL_LTCCNY, PERIOD_30MIN, his_count)
            df = pd.DataFrame(data=data, columns=['time', 'open', "high", "low", "close", "volume"])
            switch = buy_or_sell(his_api, trade_api, df, switch, acc_net, ltc, now)
        else:
            print 'WRONG WRONG'

        fileout.flush()
        inter = 10*60  # 10分钟轮回一次

        time.sleep(inter)


    his_api.exit()
    trade_api.exit()



def buy_or_sell(his_api, trade_api, df, switch, acc_net, ltc, now):
    df = df.set_index(keys=['time'])
    ma_df = kpi.get_ma(df, 4, 37, 114)

    fast_ma = 0
    slow_ma = 1

    if (ma_df.iloc[-2, fast_ma] < ma_df.iloc[-2, slow_ma]
        and ma_df.iloc[-1, fast_ma] >= ma_df.iloc[-1, slow_ma]
        and switch == 0):  # buy
        switch = 1

        data = his_api.getKline(SYMBOL_LTCCNY, PERIOD_1MIN, 5)
        buy_price = data[-1][4];
        # 估计可以买入的ltc
        ltc = round(acc_net * 1.0 / buy_price, 4)
        result = trade_api.buy(buy_price, ltc, coinType=COINTYPE_LTC)
        print 'tradebuy r:',result
        print 'tradebuy:', now, ltc, buy_price
    elif (ma_df.iloc[-2, fast_ma] > ma_df.iloc[-2, slow_ma]
          and ma_df.iloc[-1, fast_ma] <= ma_df.iloc[-1, slow_ma]
          and switch == 1):

        switch = 0
        # 估计可以卖出价格
        data = his_api.getKline(SYMBOL_LTCCNY, PERIOD_1MIN, 5)
        sell_price = data[-1][4];
        result = trade_api.sellMarket(ltc, coinType=COINTYPE_LTC)
        print 'tradesell,r',result
        print 'tradesell', now, ltc, sell_price

    return switch




if __name__ == '__main__':
    while(True):
        alpha = 1
        fileout = open('trade.txt', 'a')
        # 重定向
        sys.stdout = fileout
        sys.stderr = fileout
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print 'while for:', now
        try:
            query_and_trade(fileout)
        except Exception as e:
            print 'exception:',e

        fileout.flush()
        fileout.close()
