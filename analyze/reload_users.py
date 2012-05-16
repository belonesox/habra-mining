# -*- coding: utf-8 -*-
"""
 Building friends graph (edgelist form)
 from full habrauser DB.
"""
import sys
import os

sys.path.append('..')
from lib import MiscUtils as ut
from lib import SmartObject as so

#from ..lib import MiscUtils

USERS_DIR = '../data/users'

def reload_users():
    """
     Build friends graph 
     from full habrauser DB and
     store it as edgelist (easy readable from igraph). 
    """
    user_files_list = os.listdir(USERS_DIR) 
    for userid, filename in enumerate(user_files_list):
        user = ut.pickle2data( os.path.join(USERS_DIR, filename) )
        so_user = so.SmartObject(user)
        ut.data2pickle(so_user, os.path.join(USERS_DIR, filename))
                
   
if __name__ == '__main__':
    reload_users()
