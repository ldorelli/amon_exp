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

mpl.rcParams['font.family'] = 'Arial'

g = amon.Graph()

print 'Loading network'
g.load_directed('netw2')
print 'Loaded network, loading hashtags'
f = open('hashtags', 'r')
print 'Loaded hashtags'

l = f.readline()
tags = json.loads(l)

cm = amon.CascadeModel (g)

i_ref = { key : 0 for key in g.node_keys() }
o_ref = { key : 0 for key in g.node_keys() }

print 'Going'

for h in tags:

        v = []
        for t in tags[h]:
            v.append (t['user'])

	pr = {}
	for t in v:
		pr[t] = 1

	if len(v) < 1000:
		continue

	print 'Name ', h.encode('utf-8')
        print 'Nu ', len(v)
	print 'Probability ', len(pr)/float(g.nodes_qty())

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


	for d in range (0, 1):
		#  Two types of cascades each
		cm.run_from_record_paths(v, d + 1)
		cg = cm.cascades()

		p = cg.as_dot(True)
		f = open ('./dots/' + h.encode('utf-8') + str(d) + '.dot', 'w')
		f.write(p)
		f.close()
