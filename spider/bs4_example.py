from bs4 import BeautifulSoup
import urllib
import urllib2


def read_ctx(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason


ctx=read_ctx("http://36kr.com/")
soup = BeautifulSoup(ctx, 'lxml')
print soup.head.title.string
print soup.head.contents
print soup.find_all('a')
