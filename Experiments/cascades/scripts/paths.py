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

gg = {}
for x in g.node_keys():
    gg[x] = 1


for h in tags:
    pr = {}

    for t in tags[h]:
        pr[t]  = 1

    if len (pr) < 400:
        continue

    cm.run_from_record_paths(tags[h], 2)
    cg = cm.cascades()

    K = cg.node_keys()
    L = []
    for x in K:
        if cg.in_degree(x) == 0 and cg.out_degree(x) > 0:
            L.append(x)
    B = cg.bfs(L)
    B2 = g.bfs(L)

    for e in B:
        if e in B2:
            if B[e] > 0:
                print B[e], B2[e]
