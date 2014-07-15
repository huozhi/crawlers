# -*- coding: utf-8 -*-

import os
import ConfigParser
import urllib2
from bs4 import BeautifulSoup

leetcodeProblem = 'https://oj.leetcode.com/problems/'
confpath = 'config.cfg'

if not os.path.exists(dirpath):
    os.makedirs(dirpath)


cf = ConfigParser.ConfigParser()
cf.read(confpath)
if not cf.has_section('problem'):
    cf.add_section('problem')

problems = urllib2.urlopen(leetcodeProblem).read()
soup = BeautifulSoup(problems)
problemTable = soup.find_all("tr")[2:]

refers = []
for problem in problemTable:
    childTags = problem.find_all('td', text=True)
    title, refer = childTags[0].a.string, childTags[0].a.get('href')
    date  = childTags[1].string
    rates = childTags[2].string
    refers.append(refer[len('/problems/'):-1])

index = 1
for ref in refers:
    cf.set("problem", str(index), ref)
    index += 1

cf.write(open(confpath, 'w'))