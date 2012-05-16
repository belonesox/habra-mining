# -*- coding: utf-8 -*-
"""
 Analysis and reports about habrafriends graph.
"""
import sys
import os
from igraph import *
import numpy

sys.path.append('..')
from lib import MiscUtils as ut
from lib import HAUtils as ha


def analyze_friends():
    # pylint: disable=E1101
    sourcefile = os.path.join(ha.get_graph_dir(), 'friends.edgelist')
    thegraph = Graph.Read_Edgelist(sourcefile, directed=False)
    print "Graph loaded"
    print thegraph
    # dd = thegraph.degree_distribution() /??
    degs = thegraph.vs.degree()
    print numpy.median(degs)
    print numpy.mean(degs)
    hist = Histogram(bin_width=2)
    hist << degs
    plot(hist, os.path.join(ha.get_reports_dir(), "habrafriends-degrees-distribution.svg"))
        
                
   
if __name__ == '__main__':
    analyze_friends()
