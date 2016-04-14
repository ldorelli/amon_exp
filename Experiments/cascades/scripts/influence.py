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
g.load_directed('../netw')

print 'Loading tags'
f = open('../hashtags', 'r')
l = f.readline()
tags = json.loads(l)

cm = amon.CascadeModel (g)

n = g.nodes_qty()
R = {}
for i in range (0, 20):
    f2 = open ('../data/BET_out/output' + str(i))
    for line in f2:
        x = line.split()
        if len(x) != 2:
            continue
        if x[0] in R:
            R[int(x[0])] += float(x[1])
        else:
            R[int(x[0])] = float(x[1])

for x in R:
    R[x] /= float ( (n-2)*(n-1) )

# R = g.eigenvector_centrality(2000)
# T = g.betweenness_unw()

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
    H = {}
    T = []
    for k in tags[h]:
        if k not in H:
            T.append(k)
            H[k] = 1

    for k in T:
        if k in R:
            print v/float(len(T)), R[k]
            v += 1
