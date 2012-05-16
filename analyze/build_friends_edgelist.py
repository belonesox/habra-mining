# -*- coding: utf-8 -*-
"""
 Building friends graph (edgelist form)
 from full habrauser DB.
"""
import sys
import os

sys.path.append('..')
from lib import MiscUtils as ut
from lib import HAUtils as ha
from lib import SmartObject as so
#from ..lib import MiscUtils

def build_friends_edgelist():
    """
     Build friends graph 
     from full habrauser DB and
     store it as edgelist (easy readable from igraph). 
    """
    users_dir = ha.get_users_dir()
    user_files_list = os.listdir(users_dir) 
    user_files_list.sort()
    login2id = {}
    for userid, filename in enumerate(user_files_list):
        login = filename.split('.')[0].replace('@', '')
        login2id[login] = userid
        
    edgefile = open(os.path.join(ha.get_graph_dir(), 'friends.edgelist'), 'w')

    for userid, filename in enumerate(user_files_list):
        user = so.SmartObject(
                ut.pickle2data(os.path.join(users_dir, filename)))
        login = filename.split('.')[0].replace('@', '')
        
        if user.friends:
            for friend in user.friends:
                if friend in login2id:
                    friend_id = login2id[friend]
                    edgefile.write('%d %d\n' % (userid, friend_id) )

    edgefile.close()
                
if __name__ == '__main__':
    build_friends_edgelist()
