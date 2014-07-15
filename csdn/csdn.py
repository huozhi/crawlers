# -*- coding: utf-8 -*-

import urllib2
import os
from bs4 import BeautifulSoup
import traceback
import io

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
        self.page_count = 0
        req_url = CSDNCrawler.baseurl + "/"  + self.uname + "/" + CSDNCrawler.article
        self.soup = self.make_soup(req_url)        


    def make_soup(self, _url):
        try:
            req = urllib2.Request(
                url = _url,
                data = None,
                headers = CSDNCrawler.headers)
            res = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print "http err:", e.code
            return None
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

    def save_user_info(self):
        self.udir = "./download/" + self.uname
        if not os.path.exists(self.udir):
            os.makedirs(self.udir)
        try:
            with open(self.udir + "/blog-listst.html", "w+") as user_blog_list:
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


    def get_blog_content(self):
        title_order = 0
        try:
            for eachitem in self.blog_list:
                title_order += 1
                # get content of each blog
                blog_soup = self.make_soup(eachitem.href)
                if blog_soup == None: continue
                content = blog_soup.find("div", attrs={"class":"article_content"})
                # save content
                blog_path = "%s/%s.html" % (self.udir, str(title_order))
                self.save_blog(blog_path)
        except Exception:
            traceback.print_exc()

    def save_blog(self, blog_path):
        if not os.path.exists(path):
            with open(blog_path, "w+") as eachblog:
                eachblog.write(content.prettify().encode("gbk", "ignore"))
                print "%s's blog: %d.html saved" % (self.uname, title_order)


    def count_blog(self):
        total = self.soup.find("div",attrs={"class":"pagelist"})
        # print type(total)
        count = total.span.text.encode('gbk').split(u'条'.encode('gbk'))[0]
        # print int(count)
        self.blog_count = int(count)
        soup = BeautifulSoup(str(total))
        pages = soup.find_all('a')[-1]['href'][::-1].split('/')[0]
        # print int(pages)
        self.page_count = int(count)

    def crawl_begin_id(self):
        save_count = sum([lem(files) for root,dirs,files in os.walk(self.udir)])-1
        if save_count < self.blog_count:
            print 'unsaved files count:', self.blog_count - save_count
            return self.blog_count - save_count
        else:
            return self.blog_count

    