# -*- coding: utf-8 -*-
import os
import sys
import time
import thread
import urllib2
import cookielib
import ConfigParser
from bs4 import BeautifulSoup


# constant value
leetcodeProblem = 'https://oj.leetcode.com/problems/'
dirpath    = './download/'
configPath = 'config.cfg'
nineSolutionBaseUrl = 'http://answer.ninechapter.com/solutions/'



def saveAnswer(title):
    filename = dirpath + title + '.java'
    solutionUrl = nineSolutionBaseUrl + title + '/'
    try:
        html = urllib2.urlopen(solutionUrl).read()
        solsoup = BeautifulSoup(html)
        # summary = solsoup.find('div', class_='post-sum').string
        code = solsoup.find('pre', class_='prettyprint').string
        code = str(code).replace('\r\n','\n')
        with open(filename, 'w+') as answer:
            print filename,'opened'
            answer.write(code.encode('utf-8'))
    except urllib2.HTTPError, e:
        # print type(e.code), e.code
        if e.code == 404:
            print 'they havent upload %s answer untill now' % title
            return

def getUndownload():
    # read configuration
    cf = ConfigParser.ConfigParser()
    cf.read(configPath)
    refers = []
    undownload = []
    for item in cf.items('problem'):
        refers.append(item[1])

    for title in refers:
        filepath = dirpath + title + '.java'
        if os.path.exists(filepath):
            continue
        undownload.append(title)
    return undownload

def download(undownload):
    for title in undownload:
        try:
            saveAnswer(title)
        except Exception, e:
            print title, e
            continue
        time.sleep(3)


def main():
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    if len(sys.argv) > 1:
        answers = getUndownload()
        if sys.argv[1] == '-d':
            download(answers)
            return
        elif sys.argv[1] == '-u':
            print 'undownload list:'
            print 'you have', len(answers), 'answers undownload'
            return
        elif sys.argv[1] == '-l':
            for ans in answers: print ans
            return

    print '\nleetcode.py need args:'
    print '-d    download leetcode java answer from ninechapter'
    print '-u    check amount of undownload answers'
    print '-l    print all undownload answer titles'

if __name__ == '__main__':
    main()




