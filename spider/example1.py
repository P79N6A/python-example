
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

def printContent(ctx):
    content = ctx.decode('utf-8')
    pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="articleGender manIcon">(.*?)</div>.*?<div class="content">.*?<span>(.*?)</span>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print "auhtor:",item[0],"age:",item[1],"ctx:", item[2]

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    printContent(response.read())
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
