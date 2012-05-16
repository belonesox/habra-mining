#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  Collection of all habra-analyze specific utilities
"""
import sys
import os

import MiscUtils as ut


def get_data_dir():
    if 'HABRA_DB_PATH' in os.environ:
        return os.path.realpath(os.environ['HABRA_DB_PATH'])
    assert False  # Please, set HABRA_DB_PATH to your workspace checkouted from http://subversion.assembla.com/svn/habradata/ 
    return None


def get_graph_dir():
    thedir = os.path.join(get_data_dir(), 'graph')
    assert os.path.exists(thedir)
    return thedir

def get_users_dir():
    thedir = os.path.join(get_data_dir(), 'users')
    assert os.path.exists(thedir)
    return thedir


def get_reports_dir():
    thedir = os.path.join(get_data_dir(), 'reports')
    ut.createdir(thedir)    
    assert os.path.exists(thedir)
    return thedir
