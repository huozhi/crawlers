# -*- coding: utf-8 -*-
import urllib2
import os
from bs4 import BeautifulSoup
import traceback
import io

# import sys;
# reload(sys);
# sys.setdefaultencoding("gbk")


class ArticleItem:
    def __init__(self, _title):
        self.title = _title
        self.set_attr()
    
    def set_attr(self, _href=None, _brief=None):
        self.href = _href
        self.brief = _brief

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
        self.soup = self.make_soup(CSDNCrawler.baseurl)        


    def make_soup(self, _url):
        req_url = _url + "/"  + self.uname + "/" + CSDNCrawler.article
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
            brief = item_soup.find("div", attrs={"class":"article_description"}).get_text("|",strip=True)
            title = item_link_title.get_text("|", strip=True) # get article title
            href = CSDNCrawler.baseurl + item_link_title["href"] # get article href
            # print 'blog', count, title, href
            article = ArticleItem(title)
            article.set_attr(href, brief)
            self.blog_list.append(article)
        self.save_info()

    def save_info(self):
        udir = "csdn/" + self.uname
        if not os.path.exists(udir):
            os.makedirs(udir)
        try:
            with open(udir + "/blog-listst.html", "w+") as user_blog_list:
                # format_list = []
                # user_blog_list.write(unicode("<h4>title ------ brief ------ href</h4>\n"))
                for eachitem in self.blog_list:
                    html_item = "<a href='%s'><h2>%s</h2></a><h4>%s</h4>\n"\
                        % (eachitem.href, eachitem.title, eachitem.brief)
                    # format_list.append(html_item)
                    user_blog_list.write(html_item.encode("gbk", "ignore"))
            print "%s'blog list saved!" % self.uname
        except Exception, e:
            traceback.print_exc()






# test
def main():
    crawler = CSDNCrawler("wxg694175346")
    crawler.get_list_item()


if __name__ == '__main__':
    main()