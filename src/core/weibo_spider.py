# -*-coding:utf8-*-

import re

import string

import sys

import os

import urllib

import urllib2

from bs4 import BeautifulSoup

import requests

from lxml import etree

reload(sys)

sys.setdefaultencoding('utf-8')

if (len(sys.argv) & gt;=2):

    user_id = (int)(sys.argv[1])

else:

    user_id = (int)(raw_input(u"???user_id: "))

cookie = {"Cookie": "#your cookie"}

url = 'http://weibo.cn/u/%d?filter=1&amp;page=1' % user_id

html = requests.get(url, cookies=cookie).content

selector = etree.HTML(html)

pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

result = ""

urllist_set = set()

word_count = 1

image_count = 1

print u'??????...'

for page in range(1, pageNum + 1):

    # ??lxml??

    url = 'http://weibo.cn/u/%d?filter=1&amp;page=%d' % (user_id, page)

    lxml = requests.get(url, cookies=cookie).content

    # ????

    selector = etree.HTML(lxml)

    content = selector.xpath('//span[@class="ctt"]')

    for each in content:

        text = each.xpath('string(.)')

        if word_count & gt;= 4:

            text = "%d :" % (word_count - 3) + text + "\n\n"

        else:

            text = text + "\n\n"

        result = result + text

        word_count += 1

    # ????

    soup = BeautifulSoup(lxml, "lxml")

    urllist = soup.find_all('a', href=re.compile(r'^http://weibo.cn/mblog/oripic', re.I))

    first = 0

    for imgurl in urllist:
        urllist_set.add(requests.get(imgurl['href'], cookies=cookie).url)

        image_count += 1

fo = open("/Users/Personals/%s" % user_id, "wb")

fo.write(result)

word_path = os.getcwd() + '/%d' % user_id

print u'????????'

link = ""

fo2 = open("/Users/Personals/%s_imageurls" % user_id, "wb")

for eachlink in urllist_set:
    link = link + eachlink + "\n"

fo2.write(link)

print u'????????'

if not urllist_set:

    print u'?????????'

else:

    # ????,????????pythonimg????

    image_path = os.getcwd() + '/weibo_image'

    if os.path.exists(image_path) is False:
        os.mkdir(image_path)

    x = 1

    for imgurl in urllist_set:

        temp = image_path + '/%s.jpg' % x

        print u'?????%s???' % x

        try:

            urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(), temp)

        except:

            print u"???????:%s" % imgurl

        x += 1

print u'??????????%d??????%s' % (word_count - 4, word_path)

print u'??????????%d??????%s' % (image_count - 1, image_path)