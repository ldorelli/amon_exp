#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import amon
import amon_analytics as an
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import amon_analytics as an
import networkx as nx
import matplotlib as mpl
import sys


def getCascadeFlow (c):
    K = c.node_keys()


    v_in = {}
    v_out = {}
    c_index = 0

    for x in K:
        v_in[x] = c_index
        v_out[x] = c_index + 1
        c_index += 2

    S = c_index
    T = c_index + 1
    c_index += 2

    f = amon.NetworkFlow(c_index)
    E = 0
    for x in K:
        #  x -> out[x] : 1
        f.add_edge (v_in[x], v_out[x], 1)
        # out[x] -> sink
        if c.out_degree(x) == 0:
            E += 1
            f.add_edge (v_out[x], T, 1)
        # src -> in[x]
        if c.in_degree(x) == 0 and c.out_degree(x) > 0:

            f.add_edge (S, v_in[x], 1)
        # out[x] -> in[j]
        for j in c.adjacency(x):
            f.add_edge (v_out[x], v_in[j[0]], 1)


    return f.max_flow(S, T)

def findInterval (data, percentage, t):
    j = 0
    sz = 0
    binSz = percentage * len(data)
    for i in range (0, len (data)):
        while j < len(data) and data[j]-data[i] <= t:
            j += 1
            sz += 1
        if j-i >= binSz:
            return True
    return False

# Returns the smallest time window (% in relation to data timespam)
# in which percentage% of the data falls into
def smallestFitInterval (data, percentage):
    data = sorted(data)
    lo = 1
    r = data[-1] - data[0]
    hi = r
    while lo != hi:
        mi = (hi + lo)/2
        if findInterval (data, percentage, mi):
            hi = mi
        else:
            lo = mi + 1
    return lo/float(r)



mpl.rcParams['font.family'] = 'Arial'

g = amon.Graph()
g.load_directed('../raw/s1/netw2')
cm = amon.CascadeModel (g)


i_ref = { key : 0 for key in g.node_keys() }
o_ref = { key : 0 for key in g.node_keys() }


f = open('../raw/s1/hashtags_pl', 'r')
for line in f:

    tag = json.loads(line)
    v = []
    for t in tag['values']:
        v.append (t['user'])

	pr = {}
	for t in v:
		pr[t] = 1

    if len(pr) < 1000:
        continue

    print 'Name ', tag['name'].encode('utf-8'), len(pr)
    print 'Probability ', len(pr)/float(g.nodes_qty())
    print 'TimeIndex ', smallestFitInterval (v, 0.5)


    # P ( compartilhar | dois vizinhos compartilharam) = P ( A | B ) / P (B)
    num = 0
    den = 0

    for x in i_ref:
        i_ref[x] = 0
    for y in o_ref:
        o_ref[x] = 0

    for k in g.node_keys():
        if k in pr:
            for j in g.adjacency(k):
                i_ref[j[0]] += 1
            for j in g.adjacency(k):
                if j[0] in pr:
                    o_ref[k] += 1

    for k in g.node_keys():
	if k not in o_ref or k not in i_ref:
	    continue
	den += o_ref[k] * i_ref[k]
	if k in pr:
	    num += o_ref[k] * i_ref[k]

    if den:
        print 'CProb ', float(num)/float(den)
    else:
        print 'CProb ', 0.0


    cm.run_from_record_paths(v,  1)
    cg = cm.cascades()

    D = cg.dag_paths()

    r = 0.0
    for x in D:
        r += D[x]

    print 'ConnectedElements ', cg.nodes_qty()/float(len(pr))

    print 'DisjointPaths' , getCascadeFlow (cg)

    if cg.nodes_qty() != 0:
        print 'Average#Paths ', r/float(len(D))
    else:
        print 'Average#Paths ', 0

    T = g.cascade_centrality (cg)
    print 'CascadeCentrality ', T[0]
    print 'NetworkCentrality ', T[1]

# Distance to source
    K = cg.node_keys()
    L = []
    for x in K:
        if cg.in_degree(x) == 0:
            L.append(x)
    B = cg.bfs(L)

    m = 0
    m2 = 0
    for x in B:
        m = max(m, B[x])
        m2 += B[x]

    print 'MaxDistance ', m
    print 'AverageDistance ', m2/float(len(B))

    p = cg.as_dot(True)
    dot_file = open ('../dots/' + tag['name'].encode('utf-8') + str(0) + '.dot', 'w')
    dot_file.write(p)
    dot_file.close()
