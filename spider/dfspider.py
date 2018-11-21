# -*- coding: utf-8 -*-
import json
import re

import requests
from copyheaders import headers_raw_to_dict
import pandas as pd
import numpy as np
import matplotlib
#import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import math

post_headers_raw = b'''
Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Cache-Control:no-cache
Connection:keep-alive
DNT:1
Host:emweb.securities.eastmoney.com
Pragma:no-cache
Referer:http://emweb.securities.eastmoney.com/FinanceAnalysis/Index?type=web&code=sh603180
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
X-Requested-With:XMLHttpRequest
'''


# #解决中文显示乱码
# matplotlib.use('qt4agg')
# #指定默认字体
# matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# matplotlib.rcParams['font.family']='sans-serif'
# #解决负号'-'显示为方块的问题
# matplotlib.rcParams['axes.unicode_minus'] = False

# 把header转化为字典类型
header_dict = headers_raw_to_dict(post_headers_raw)
common_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


class dfspider:
    def __init__(self,code,name):
        # 构造session ，用于存储browser和server交互之间的cookie
        self.session = requests.session();
        self.data = {};
        self.data['code']=code;
        self.data['name']=name;
        # 任意相关url
        init_url = 'http://emweb.securities.eastmoney.com/FinanceAnalysis/Index?type=web&code=sh603180#';
        ctx = self.session.get(url=init_url, headers=header_dict);
        # print 'ctx:'+ctx.content;
        print(ctx.headers);
        print(ctx.cookies);

    # 根据名字得到code，返回tuple(0,1)
    def get_security_code(self, name):
        self.data['name'] = name;
        pass

    def __parse_annual_data(self):
        ctx_url = 'http://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/MainTargetAjax?code=' + self.data['code'] + '&type=1';
        ctx = self.session.get(url=ctx_url, headers=header_dict);
        print ('data_ctx_y:' , ctx.content);
        if (ctx.content != None):
            list = json.loads(ctx.content)['Result'];
            self.data['A'] = self.__parseDataToDataFrame(list);
        else:
            return None;


    def __parse_season_data(self):
        ctx_url = 'http://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/MainTargetAjax?code=' + self.data['code'] + '&type=2' ;
        print(ctx_url)
        ctx = self.session.get(url=ctx_url, headers=header_dict);
        print ('data_ctx_s:' , ctx.content);
        if (ctx.content != None):
            list = json.loads(ctx.content)['Result'];
            self.data['S'] =self.__parseDataToDataFrame(list);
        else:
            return None;

    def __parseDataToDataFrame(self,list):
        cols = ['date', 'yyzsr', 'gsjlr', 'kfjlr', 'yyzsrtbzz', 'gsjlrtbzz', 'kfjlrtbzz','jll', 'jbmgsy'];
        df = pd.DataFrame(columns=cols, index=np.arange(0, len(list)));
        for idx, obj in enumerate(list):
            for col in cols:
                df[col][idx] = self.__filterField(obj[col],col);
        df = df.sort_values(by='date')
        df = df.set_index('date')
        return df;

    def __filterField(self,value,col):
        if(value=='--'):
            return 0.0;
        if(u'万' in value):
            return float(re.sub(u'万','',value))/10000;
        if (u'亿' in value):
            return float(re.sub(u'亿','',value));
        if('tbzz' in col):
            if(float(value)>100):
                return 100.0;
        return value;

    # code只要数字即刻，不需要前缀
    def __parse_institution_data(self):
        url = 'http://stockpage.10jqka.com.cn/' + self.data['code'] + '/position/';
        print(url)
        inst_data = requests.get(url, headers=common_header);
        #print inst_data.content;
        id = re.search('<th width="120px">主力进出\\\报告期</th>.*?<th>(.*?)</th>.*?<th>(.*?)</th>', inst_data.content, re.S);
        ir = re.search('<th class="tl f12">持仓比例</th>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', inst_data.content, re.S);
        ic = re.search('<th class="tl f12">机构数量\(家\)</th>.*?<td>(\d+)\t*</td>.*?<td>(\d+)\t*</td>', inst_data.content,
                       re.S);
        self.data['I'] = [id.group(1) +':' + ir.group(1) + '(' + ic.group(1) + ')', id.group(2)+':'+ir.group(2) + '(' + ic.group(2) + ')'];

    def printData(self):

        cdata = '';
        adata = '';
        idata='';
        for p in self.data['C']:
            cdata  = cdata +p[0] + ':' + p[1] + '-' + p[2] + '-' + p[4] + '</br>';
        for p in self.data['A']:
            adata =adata+ p[0] + ':' + p[1] + '-' + p[2] + '-'  + p[4] + '</br>';
        for p in self.data['I']:
            idata =idata+ p+'</br>';

        print (self.data);
        tr = '<tr><td>'+self.data['code']+'</td><td>' \
                + cdata + '</td><td>'\
                + adata + '</td><td>'\
                + 'new</td><td>'\
                + 'share</td><td>'\
                +  'leader</td><td>'\
                +  idata+'</td></tr>';

        page='''
         <html>
            <body>
                <table border="1">
                  <tr>
                    <th>code</th>
                    <th>C</th>
                    <th>A</th>
                    <th>N</th>
                    <th>S</th>
                    <th>L</th>
                    <th>I</th>
                  </tr>
         '''+tr+'''     
                </table>
            </body>
         </html>';
        '''
        fo = open("code.htm", "w+")
        fo.write(page);

        # 关闭打开的文件
        fo.close()

    def process(self):
        #self.__parse_annual_data();
        #self.__parse_season_data();
        self.__parse_institution_data();
        print (self.data);

    def show(self):

        adf=self.data['A'];
        sdf=self.data['S'];
        fig = plt.figure();
        self.__plot(fig,211,adf,self.data['name']+u'年度数据');
        self.__plot(fig,212,sdf, self.data['name'] + u'季度数据');

        #plt.gcf().autofmt_xdate()
        plt.savefig("sh603180.png",dpi=100)
        plt.show();

    def __plot(self,fig,order,adf,title):

        ax1 = fig.add_subplot(order)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # ax1.xaxis.set_major_locator(mdate.DayLocator())
        xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in adf.index.values]

        # cols = ['date', 'yyzsr', 'gsjlr', 'kfjlr', 'yyzsrtbzz', 'gsjlrtbzz', 'kfjlrtbzz', 'jbmgsy'];
        ax1.plot(xs, adf['yyzsr'].values, 'gs-', label=u'收入')
        ax1.plot(xs, adf['gsjlr'].values, 'go-', label=u'归属净利润')
        ax1.plot(xs, adf['kfjlr'].values, 'g<-', label=u'扣非净利润')
        ax1.set_ylabel(u'收入和利润(亿)')
        ax1.set_title(title)
        ax1.set_xticks(xs);
        ax1.legend(loc=2);

        # 计算复合增长率
        #CAGR= math.pow(float(adf['gsjlrtbzz'][-1]) *1.0 / adf['gsjlrtbzz'][0], 1/len(xs))-1;
        #CAGR=CAGR*100;

        ax2 = ax1.twinx()  # this is the important function
        ax2.plot(xs, adf['yyzsrtbzz'].values, 'ks-', label=u'收入增长率')
        ax2.plot(xs, adf['gsjlrtbzz'].values, 'ro-', label=u'归属净利润增长率')
        ax2.plot(xs, adf['kfjlrtbzz'].values, 'r<-', label=u'扣非净利润增长率')
        ax2.plot(xs, adf['jll'].values, 'y*:', label=u'净利率')
        ax2.set_ylim(0, 100);
        ax2.set_yticks(np.arange(0,100,5))
        #归属净利润平均增长率
        #meanRate=adf['gsjlrtbzz'][1:].mean();
        #print meanRate;
        #ax2.hlines(meanRate, colors="m", linestyles="-")
        ax2.set_ylabel(u'同比增长率%')
        ax2.set_xlabel(u'日期')
        ax2.grid(True, linestyle="-", color="darkgray", linewidth="1")
        ax2.legend(loc=9);




if __name__ == '__main__':
    df = dfspider('sz000860',u's顺心农业');#sh603180
    df.process();
    #df.show();


