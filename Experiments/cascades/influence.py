#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import amon
import sys
import amon_analytics as an
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import amon_analytics as an
import networkx as nx
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Arial'

g = amon.Graph()

print 'Loading network'
g.load_directed('netw')

print 'Loading tags'

f = open('hashtags', 'r')
l = f.readline()
tags = json.loads(l)

print 'Loading graph '

print g.nodes_qty(), g.edges_qty()

cm = amon.CascadeModel (g)
# R = g.eigenvector_centrality(1000)
T = g.betweenness_unw()

for h in tags:
    pr = {}
    for t in tags[h]:
        pr[t] = 1
    if len(pr) < 200:
        continue

    #  Run with 1
    cm.run_from_record_paths(tags[h], 1)
    cg = cm.cascades()

    v = 0
    for k in tags[h]:
        if k in R:
            print v/float(len(tags[h])), R[k]
            v += 1
