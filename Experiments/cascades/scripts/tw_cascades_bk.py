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

g.load_directed('netw')


f = open('hashtags', 'r')
l = f.readline()
tags = json.loads(l)
# print 'Loaded graph'
# print g.nodes_qty(), g.edges_qty()

cm = amon.CascadeModel (g)


i_ref = { key : 0 for key in g.node_keys() }
o_ref = { key : 0 for key in g.node_keys() }

for h in tags:

	pr = {}
	for t in tags[h]:
		pr[t] = 1

	if len(pr) < 200:
		continue

	print 'Name ', h.encode('utf-8')

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

	for d in range (0, 2):
		#  Two types of cascades each
		cm.run_from_record_paths(tags[h], d + 1)
		cg = cm.cascades()

		D = cg.dag_paths()
		r = 0.0
		for x in D:
			r += D[x]

		if cg.nodes_qty() != 0:
			print 'Average#Paths ', r/float(len(D))
		else:
			print 'Average#Paths ', 0

		# Cascade centrality on the cascade
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
		f = open ('./dots/' + h.encode('utf-8') + str(d) + '.dot', 'w')
		f.write(p)
		f.close()
