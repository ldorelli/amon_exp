#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import amon
import networkx as nx
import sys

g = amon.Graph()

print 'Loading network'
g.load_directed('netw')

print 'Loading tags'

f = open('hashtags', 'r')
l = f.readline()
tags = json.loads(l)

print g.nodes_qty(), g.edges_qty()
cm = amon.CascadeModel (g)

R = {}
i = 0
K = g.node_keys()
for x in K:
    print >> sys.stderr,  round (i/float(len(K)), 2)
    R[x] = g.bfs (x)
    i += 1
