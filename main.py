# -*- coding: utf-8 -*-

from crawlers import CSDNCrawler

def main():
    crawler = CSDNCrawler("wangyuquanliuli")
    crawler.get_list_item()
    # crawler.get_content()
    crawler.count_blog()


if __name__ == '__main__':
    main()