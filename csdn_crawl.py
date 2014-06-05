# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

class ArticleItem:
    def __init__(self, _title):
        self.title = _title
        self.brief = None
        self.href = None
        self.author = None
    
    def set_href(self, _href):
        self.href = _href

class CSDNCrawler:
    baseurl = "http://blog.csdn.net"
    article = "article"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

    def __init__(self, uname):
        self.uname = uname
        self.blog_list = []
        self.blog_count = 0
        self.soup = self.make_soup()        


    def make_soup(self):
        req_url = CSDNCrawler.baseurl + "/" \
            + self.uname + "/" + CSDNCrawler.article
        req = urllib2.Request(
            url = req_url,
            data = None,
            headers = CSDNCrawler.headers)
        res = urllib2.urlopen(req)
        return BeautifulSoup(res.read())

    def get_blogs_href(self):
        titles = self.soup.find_all("span", attrs={"class":"link_title"})
        for each_title in titles:
            blog_href = CSDNCrawler.baseurl + each_title.contents[0].get("href")
            self.blog_list.append(blog_href)
            print blog_href
            
    def get_list_item(self):
        list_items = self.soup.find_all("div", attrs={"class":"list_item article_item"})
        count = 0
        for each_item in list_items:
            count += 1
            item_soup = BeautifulSoup(str(each_item))
            item_link_title = item_soup.find("span",attrs={"class":"link_title"}).contents[0]
            title = item_link_title.get_text("|", strip=True) # get article title
            href = CSDNCrawler.baseurl + item_link_title["href"] # get article href
            print 'blog', count, title, href
            # article = ArticleItem(item_title)
            # article.set_href(href)
            # self.blog_list.append(article)



# test
def main():
    crawler = CSDNCrawler("wxg694175346")
    crawler.get_list_item()


if __name__ == '__main__':
    main()