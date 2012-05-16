#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crawling of all habrausers.
"""
import sys
import crawl_user as cu
import os

sys.path.append('..')
from lib import MiscUtils as ut

def crawl_users():
    """
    Crawl all habrausers, enumerating habrakarma pages.
    """
    page_num = 1
    users = set()
    def flush_userbase():
        ut.data2pickle(users, '../data/allusers.dat')
        for user in users:
            user = user.replace('\n', '')
            filename = '../data/users/' + user + '@.dat'
            if not os.path.exists(filename):
                print 'crawling user: <%s>' % user
                user_data = cu.crawl_user(user)
                ut.data2pickle(user_data, filename)

    if 0:
        while True:
            url_to_parse = 'http://habrahabr.ru/people/page%d/' % page_num  
            root    = ut.doc4url(url_to_parse)
            if not root:
                break
            items = root.xpath('//div[@class="username"]//a')
            print 'Page = ', page_num
            if len(items) > 0:
                new_users =  set([ut.unicodeanyway(node.text)
                                 for node
                                    in items])
                users.update(new_users)
            page_num += 1
    users = ut.pickle2data('../data/allusers.dat')
        #if page_num % 1000 == 0:
        #    flush_userbase()

    flush_userbase()
    
    
if __name__ == '__main__':
    crawl_users()
