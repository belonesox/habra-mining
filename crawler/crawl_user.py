#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crawling of single habrauser.
"""

import sys

sys.path.append('..')
from lib import MiscUtils as ut
from lib import SmartObject as so

def crawl_user(username):
    """
     Crawl habrauser info,
     return dictionary with these attributes.
    """
    url_to_parse = 'http://habrahabr.ru/users/' + username + '/' 
    root    = ut.doc4url(url_to_parse)

    def get_set(css_class_name, set_num=0):
        """
        Find in the page list of some hyperlinked properties
        (such as friends, interests, etc)
        and return a set of them.
        """
        if not root:
            return None
        item = root.xpath('//dl[@class="%s"]/dd' % css_class_name)
        if len(item) <= set_num:
            return None
        sets_node  = item[set_num]
        item_set = set([ut.unicodeanyway(node.text).replace('\n', '')
                         for node
                            in sets_node.xpath('.//a') if node.text is not None])
        
        
        
        return item_set

    user = so.SmartObject({
        'interests' : get_set('interests'),
        'companies' : get_set('companies_list'),
        'friends' :  get_set('friends_list'),
        'hubs' : get_set('hubs_list'),
        'invitees': get_set('friends_list', 1)
    })    
    return user
    
    
def smoke_test():
    """
    Simple smoke/acceptance test.
    Crawl user info, store them in pickle file.
    """
    habrauser = 'belonesox'
    user = crawl_user(habrauser)
    print user
    ut.data2pickle(user, '../data/users/' + habrauser + '.dat')
    
if __name__ == '__main__':
    smoke_test()