# -*- coding: utf-8 -*-
import requests
import re
import json
from copyheaders import headers_raw_to_dict

post_headers_raw=b'''
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

#把header转化为字典类型
header_dict= headers_raw_to_dict(post_headers_raw)



class dfspider:

    def __init__(self):
        # 构造session ，用于存储browser和server交互之间的cookie
        self.session=requests.session();
        self.data={};
        # 任意相关url
        init_url = 'http://emweb.securities.eastmoney.com/FinanceAnalysis/Index?type=web&code=sh603180#';
        ctx=self.session.get(url=init_url,headers=header_dict);
        #print 'ctx:'+ctx.content;
        print ctx.headers;
        print ctx.cookies;

    def get_annual_data(self,code,type):
        ctx_url='http://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/MainTargetAjax?code='+code+'&type='+type;
        ctx=self.session.get(url=ctx_url,headers=header_dict);
        print 'data_ctx:'+ctx.content;
        if(ctx.content!=None):
             list=json.loads(ctx.content)['Result'];
             count=0;
             ts=[];
             for obj in list:
                 if(count==3):
                     break;
                 tuple=(obj['date'],obj['yyzsrtbzz'],obj['kfjlrtbzz']);
                 ts.append(tuple);
                 count+=1;
             self.data['A']=ts;
        else:
         return None;

    def get_season_data(self,code,type):
        ctx_url='http://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/MainTargetAjax?code='+code+'&type='+type;
        ctx=self.session.get(url=ctx_url,headers=header_dict);
        print 'data_ctx:'+ctx.content;
        if(ctx.content!=None):
             list=json.loads(ctx.content)['Result'];
             count=0;
             ts=[];
             for obj in list:
                 if(count==3):
                     break;
                 tuple=(obj['date'],obj['yyzsrtbzz'],obj['gsjlrtbzz'],obj['kfjlrtbzz'],obj['jbmgsy']);
                 ts.append(tuple);
                 count+=1;
             self.data['C']=ts;
        else:
         return None;

    def printData(self):
        print 'data',self.data;

if __name__ == '__main__':
    df=dfspider();
    df.get_annual_data('sh603180','1')
    df.get_season_data('sh603180','2')
    df.printData();
