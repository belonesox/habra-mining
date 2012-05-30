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
import numpy as np

#from ..lib import MiscUtils

def cut_thread(postpath):
    """
      Build a graph matrix, set MAX-CUT problem
    """
    thepostsdir = os.path.join(ha.get_data_dir(), 'posts')
    filename = os.path.join(thepostsdir, postpath) + '.dat'
    thread_tree = ut.pickle2data(filename)
    
    def walk_tree_for_login2id(subtree, login2id):
        for login in subtree:
            if login not in login2id:
                login2id[login] = len(login2id) 
            walk_tree_for_login2id(subtree[login], login2id)
            
    login2id = {}
    walk_tree_for_login2id(thread_tree, login2id)
    
    N = len(login2id)
    weights = np.zeros((N, N), dtype=np.int16)

    def walk_tree_for_weights(root_login, subtree, weights):
        u = login2id[root_login]
        for login in subtree:
            v =  login2id[login]
            if u != v:
                weights[u, v] += 1
                weights[v, u] += 1
                walk_tree_for_weights(login, subtree[login], weights)
    
    for root_login in thread_tree:
        walk_tree_for_weights(root_login, thread_tree[root_login], weights)

    id2login = {}
    for login in login2id:
        id2login[login2id[login]] = login

    y = greedy_max_cut(weights)

    def print_habrauser(uid):
        login = id2login[uid]
        print '* [http://' +  login + '.habrahabr.ru ' + login + ']'

    print "Analysis of http://habrahabr.ru/" + postpath
    print "----"
    print "Party 1"
    for i in xrange(N):
        if y[i] > 0:
            print_habrauser(i)

    print "----"
            
    print "Party 2"
    for i in xrange(N):
        if y[i] < 0:
            print_habrauser(i)
            
    print "----"
    


def greedy_max_cut(weights):
    N = weights.shape[0]
    y = np.ones(N, dtype=np.int8)
    while True:
        inadequacy = y * np.dot(weights, y)
        indeadequate = np.argmax(inadequacy)
        if inadequacy[indeadequate] <= 0:
            break
        y[indeadequate] *= -1

    return y    
                    
if __name__ == '__main__':
    cut_thread('post/144768')
    #weights = np.array([[0,2,4,1],
    #                    [2,0,1,1],
    #                    [4,1,0,1],
    #                    [1,1,1,0]])
    #
    #greedy_max_cut(weights)