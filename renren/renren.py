# -*- coding: utf-8 -*-

import urllib2
import cookielib
from bs4 import BeautifulSoup

cookies = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookies, urllib2.HTTPHandler)
urllib2.install_opener(opener)

rr_users = {
    "dongbeilinux":"http://page.renren.com/601754395"
}
req = urllib2.Request(
    url = rr_users["dongbeilinux"]
    )
html = opener.open(req).read()


soup = BeautifulSoup(html)
status = soup.find_all("span", attrs={"class":"status-detail"})
with open('./download/dongbeilinux.html','w+') as html:    
    for state in status:
        details = (state.get_text() + '<br/><br/>').encode('gbk')
        html.write(details)
