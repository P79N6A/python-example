# -*- coding: utf-8 -*-
import requests
import sys
import io
import json

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

#登录后才能访问的网页
url = 'http://powerlog.alibaba-inc.com/indx.html#/dashboard/file/detail.json?app=wdkitem'


#设置请求头
mheaders = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Content-Type':'application/json;charset=UTF-8'}

#浏览器登录后得到的cookie，也就是刚才复制的字符串
cookie_str = r'lg=true; sg=j06; UM_distinctid=1566d5883d4176-05a0a9171b20d7-133f6f55-fa000-1566d5883d5149; new_openwork_feedback_animate=true; cna=An8vEIGjRD0CAXkAHd3AMFdG; ck2=b3d67ac649ae2991c1d4394fedf43cfa; an=Pengju.zpj; bs_n_lang=zh_CN; l=AqmphQdZp9ETj7Fsu05PMUuiOV4Ddp2o; emplId=72106; c_token=d930fd0113ff10137784d3eb1e0b1a48; cn_1260001221_dplus=%7B%22distinct_id%22%3A%20%221566d5883d4176-05a0a9171b20d7-133f6f55-fa000-1566d5883d5149%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201519453175%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201519453175%7D%7D; hrc_sidebar=open; lvc=sAhtq8p8FqBSng%3D%3D; powerlog_USER_COOKIE=B234A77178EC090EF3364F9C867F456454086DA0CB21177A8768741AE3CD4933888853F8F8DE2B0EEBDAAADB07D5896B013E6FBABC0F688D57C8D0750969AB5D80E6624B34B44BA9F41EDF7A70B8C3BD6E9460727C22C0CB8CF59375E6D43B9E71C2654FB4492331016A3C7D6E28D4CAADE1723C572EA08205EC2895E17EB2FB5CBC283229A30CAF73A35985615ADA2D38045C87A66C2A5E2DEC89E977A680F20A88BB2417B9B3B4A6D5FE7C71B721D3D386808B1F4020DAC789D12BB4C35F90C84E465A71405BC6B911CA44AD59760CAC5E2C502508DE376090764700EED9DC3CA3951A71C2E370D398A47254EF1B7ACE758DA5A1082EFF8D48C522D7EB3BA3DCF8C937CE9D343A569C1FF80D74361090D9715B8C7F9531F19528D1B6428B86CAB7D1DD2F8BA8C68CC1E82241986E435758C5F7631D27132C7C372420CF2D08B85C5905E96CAC74AD5B8BF8667FE0CFE55857B41B5E7DEC09EA559FA084C04365F8EEEB965216963A76AD47824B068853E6FD6025B96013803B3E32A9A3AE85855A39DE93D5AC49A613AF44BD34B579C6EF3AFF731408D6A75DA7B2FD81B8FE; SSO_EMPID_HASH=e358393a01eb612dced10fdbecc41994; SSO_LANG=; powerlog_SSO_TOKEN=E2BA2B1435BC155459B2024608E3D915D470048B30EB261BF721834F64E9601B65D9424321DA4A2E7A4E79B0B1D789F9; powerlog_LAST_HEART_BEAT_TIME=1A9E28E0D0E0B1F10CA3AD93C4740DAD; isg=BCAgnwKLbvJn-NG6oEXzR5Fi8SjsLyyXVaBofJozEDpVlca_QjlFgn1tKTUVJbzL'
#把cookie字符串处理成字典，以便接下来使用
mcookies = {}
for line in cookie_str.split(';'):
    key, value = line.split('=', 1)
    mcookies[key] = value


# 在发送get请求时带上请求头和cookies
#resp = requests.get(url, headers=mheaders, cookies=mcookies)
#print(resp.content.decode('utf-8'))
#print('-----')



#登录时需要POST的数据
mdata = '{"query":{"filtered":{"query":{"bool":{"should":[{"query_string":{"query":"0ab01f6615194638206315277d858e"}}]}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"from":1519442362476,"to":1519463962476}}}]}}}},"highlight":{"fields":{},"fragment_size":2147483647,"pre_tags":["@start-highlight@"],"post_tags":["@end-highlight@"]},"size":1000,"sort":[{"_score":{"order":"asc","ignore_unmapped":true}}]}|biz-digest#';
post_url='http://powerlog.alibaba-inc.com/detail/_search.do?app=wdkitem'
#构造Session
session = requests.Session()
#在session中发送登录请求，此后这个session里就存储了cookie
print(session.cookies.get_dict())
resp = session.post(post_url, data=mdata,headers=mheaders)
ctx=resp.content.decode('utf-8');
print(ctx)
pctx=json.loads(ctx);
print  pctx['hits']['hits'][0]['_source']
