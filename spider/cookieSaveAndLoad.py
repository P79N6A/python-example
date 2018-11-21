# -*- coding: utf-8 -*-
'''

import urllib
import urllib2

httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
urllib2.install_opener(opener)

url = 'https://www.zhihu.com/api/v4/questions/20267239/answers?include=data%5B*%5D.is_normal%2Cis_collapsed%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=3&limit=20&sort_by=default'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36)'
referer='https://www.zhihu.com/question/20267239'
cookie='Cookie:d_c0="AADA9HiLWwqPTnuQwyaIho_9LEce_W8WBdE=|1470722160"; _za=82e18529-9072-465c-b98c-cc63e06ce880; _zap=4fb9799c-4cfc-4c4d-a01a-c73b96798175; _xsrf=ff4971954a19ec2d2a359ecf5a659be9; aliyungf_tc=AQAAAHrqFidv3QgA3R0AeZIwFGOaw2lj; _ga=GA1.2.776232368.1484815551; acw_tc=AQAAAJmtOBibdw4A3B0AeYhHSH7GQXdC; capsion_ticket=a6ff78f712e64decace3a7c4c79cf538; q_c1=e0b05edd1c2b4685b68077a9c1eb9a6e|1496373019000|1470722160000; s-q=scikit%20lean; s-i=3; sid=c3qq54a8; r_cap_id="OTllMTNiODAyMjM2NGMzY2IyNzdkNWE0ZDg4NGRkMjQ=|1497411196|b1dcf34da9dbc01a36fa855981d994592157bd03"; cap_id="MTc0MTEwMjYwYjE2NDE2M2E5ZWZlODhjYTk1NDdmMTk=|1497411196|e339a45c9f1547bdc820d3b91249b151bcfc6336"; __utma=51854390.776232368.1484815551.1496910143.1497411198.2; __utmc=51854390; __utmz=51854390.1497411198.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|2=registration_date=20151009=1^3=entry_date=20160809=1; z_c0=Mi4wQUJDTVRsVEQwZ2dBQU1EMGVJdGJDaGNBQUFCaEFsVk5menRvV1FCdWFKUlJwVHF1NWtVQXMtemhzaV9mZndmeHFB|1497498302|c4f0c08db6ad54235bccf310eb53c8a4e24d836d'
authorization='Bearer Mi4wQUJDTVRsVEQwZ2dBQU1EMGVJdGJDaGNBQUFCaEFsVk5menRvV1FCdWFKUlJwVHF1NWtVQXMtemhzaV9mZndmeHFB|1497498302|c4f0c08db6ad54235bccf310eb53c8a4e24d836d'
#values = {'username': 'cqc', 'password': 'XXXX'}
headers = {'User-Agent': user_agent,'Referer':referer,'Cookie':cookie,'authorization':authorization}
#data = urllib.urlencode(values)

request = urllib2.Request(url, None, headers)
print request.get_method()
response = urllib2.urlopen(request)
page = response.read()
print page
'''

import urllib2
import cookielib

def visitWebAndSaveCookie(url):
    #设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'cookie.txt'
    #声明一个CookieJar对象实例来保存cookie
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler=urllib2.HTTPCookieProcessor(cookie)
    #通过handler来构建opener
    opener = urllib2.build_opener(handler)
    #此处的open方法同urllib2的urlopen方法，也可以传入request
    response = opener.open(url)
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value

    #保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)


def loadCookieAndVisitWeb(url):
    # 创建MozillaCookieJar实例对象
    cookie = cookielib.MozillaCookieJar()
    # 从文件中读取cookie内容到变量
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    # 创建请求的request
    req = urllib2.Request(url)
    # 利用urllib2的build_opener方法创建一个opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    print response.read()

def main():
    url='http://www.baidu.com'
    visitWebAndSaveCookie(url)
    loadCookieAndVisitWeb(url)

    import re
    pattern = re.compile(r'\d+')
    print re.findall(pattern, 'one1two2333three3four4')

main()


