# -*- coding: utf-8 -*-
import requests
import re
import json

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

#构造Session
session = requests.Session()

#登录后才能访问的网页
loginUrl = 'https://www.zhihu.com'
signPostUrl='https://www.zhihu.com/api/v3/oauth/sign_in';


#设置请求头
mheaders = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Content-Type':'application/text;charset=UTF-8'}



r = session.get(loginUrl)
html = r.text
print html
print '----------------'
#p1 = re.search(r'<input type=\"hidden" name="umidTokenId\" value="(.*?)" >',html)
#umidTokenId= p1.group(1)
#print 'umidTokenId:'+umidTokenId;

mdata={
    'account':'492970b2d5675dec458f55de7d1dd557dbf693b1e06e983135acd4e27b0fe93952fcdc1866d9263eea88e4fca109d2c373a5b60b7ec497412916d203312cdbf86bad5328f7918ce840635ce465e06189f347e3379dc769743b26c48484331cc7d5b4c7345e558299417ada7158265e02a2030bb6352285a26f1b19f5d404fe85',
    'password':'6b9c1bdd6c93a92b7e52fedc5bda0385e164fc037a4868473e2519742fa28f424a4b30cdc03337b4ca2ef108448bc8e3b16b2aa9eccece2f5f9866e67a0eb0aaa480f5356e1bafec3da37513de0982d6a3c67f5f6fc4fe94fa5d889f16c64c1ee2406144cc18827ae6cfb1a7f9dfbdebc6c07ca444ea9d48dd835f975f80d9b6',
    'tbCheckCode':'',
    'rsaToken':'',
    'loginType':'ACCOUNT',
    '_sso_csrftoken':'kMu2NfmTZNr',
    #'umidTokenId':umidTokenId,
    'phoneNumToken':'1c3cee6d-f204-4237-b86c-6db5061b3c23',
    'deviceIp':'552c88fde72a6c3c296e1a588fe825f79864f075343cf9252ac3e1396c2946aa8a9b42dc6594ad38d6a01e9f66f36748',
    'isRsaPwd':True,
    'login_maintain':True,
    'keepLogged':True
}

#p1 = re.compile(r'city_token" value="(.*?)"')
#res = re.search(p1,html)

r = session.post(signPostUrl, data=mdata,headers=mheaders)

print r.request.headers
print session.cookies

# 在发送get请求时带上请求头和cookies
#resp = requests.get(url, headers=mheaders, cookies=mcookies)
#print(resp.content.decode('utf-8'))
#print('-----')



