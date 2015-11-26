#!/usr/bin/python

from igraph import *
import amon
import sys
import random

def gen_community(n = 264, m = 8, k_in = 12, k_out = 3):
	ein = []
	eout = []
	for i in range(m):
		ein.append([])
		eout.append([])
		for j in range(0, n/m):
			for k in range(k_in):
				ein[i].append((n/m)*i + j)
			for k in range(k_out):	
				eout[i].append((n/m)*i + j)

	edges = {}
	E = []
	#  Generates the IN part
	for i in range(m):
		while len(ein[i]) > 1:
			a = random.randint(0, len(ein[i])-1)
			e1 = ein[i][a]
			del ein[i][a]
			b = random.randint(0, len(ein[i])-1)
			e2 = ein[i][b]
			# print e1, e2
			del ein[i][b]
			if (e1, e2) not in edges and (e2, e1) not in edges:
				edges[(e1, e2)] = 1
				E.append((e1, e2))

	# Generates the out part
	for i in range(m):
		j = 0
		explod = 0
		while len(eout[i]) and explod < 3:
			if len(eout[j]) != 0:
				a = random.randint(0, len(eout[i])-1)
				b = random.randint(0, len(eout[j])-1)
				e1 = eout[i][a]
				e2 = eout[j][b]
				del eout[i][a]
				del eout[j][b]
				if (e1, e2) not in edges and (e2, e1) not in edges:
					edges[(e1, e2)] = 1
					E.append((e1, e2))
				explod = 0
			else: 
				explod += 1
			j = (j+1)%m
			if j == i:
				j = (j+1)%m

	return Graph(E)


c1 = [ 'out.random',  'moreno_propro/out.moreno_propro_propro', 'euroroad/subelj_euroroad/out.subelj_euroroad_euroroad', 'arenas-email/out.arenas-email', 'hamster/out.petster-friendships-hamster-uniq' ]


for net_file in c1:
	print net_file

	if net_file != 'out.random':
		# Using amon.Graph to load and igraph to calculate communities
		h = amon.Graph()
		h.load_undirected(net_file)

		print 'Loading'
		# WTF igraph is really slow
		E = {}
		edges = []
		for x in h.node_keys():
			for y in h.adjacency(x):
				a = h.node_index(x)
				b = h.node_index(y[0])
				if (a, b) not in E and (b, a) not in E:
					E[(a, b)] = 1
					edges.append((a, b))
		print 'Loaded'
		g = Graph(edges)
	else:
		g = gen_community()

	d = g.components(WEAK)
	b = Graph()
	for k in d.subgraphs():
		if len(k.vs) > len(b.vs):
			b = k 
	print len(b.vs), len(g.vs)
	g = b

	# Fast Greedy
	c = Graph.community_fastgreedy(g).as_clustering()
	for i in range (0, len(c.membership)):
		g.vs[i]['com'] = c.membership[i]
	i = 0
	for e in g.get_edgelist():
		if c.membership[e[0]] != c.membership[e[1]]:
			g.es[i]["weight"] = 3
		else:
			g.es[i]["weight"] = 1
		i += 1
	pos = net_file.find("out.")
	net = "results3/" + net_file[pos+4:]
	f = open(net + '_fast_greedy_' + '.dot', 'w+')
	g.write_dot(f)
	print c.modularity
	f.close()

	# Eigenvector
	c = Graph.community_leading_eigenvector(g) #.as_clustering()
	for i in range (0, len(c.membership)):
		g.vs[i]['com'] = c.membership[i]
	i = 0
	for e in g.get_edgelist():
		if c.membership[e[0]] != c.membership[e[1]]:
			g.es[i]["weight"] = 3
		else:
			g.es[i]["weight"] = 1
		i += 1
	pos = net_file.find("out.")
	net = "results3/" + net_file[pos+4:]
	f = open(net + '_leading_eigenvector_' + '.dot', 'w+')
	g.write_dot(f)
	print c.modularity
	f.close()

	# Edge Betweenness
	c = Graph.community_edge_betweenness(g).as_clustering()
	for i in range (0, len(c.membership)):
		g.vs[i]['com'] = c.membership[i]
	i = 0
	for e in g.get_edgelist():
		if c.membership[e[0]] != c.membership[e[1]]:
			g.es[i]["weight"] = 3
		else:
			g.es[i]["weight"] = 1
		i += 1
	pos = net_file.find("out.")
	net = "results3/" + net_file[pos+4:]
	f = open(net + '_leading_eigenvector_' + '.dot', 'w+')
	g.write_dot(f)
	print c.modularity
	f.close()
	
	# Walktrap
	c = Graph.community_walktrap(g).as_clustering()
	for i in range (0, len(c.membership)):
		g.vs[i]['com'] = c.membership[i]
	i = 0
	for e in g.get_edgelist():
		if c.membership[e[0]] != c.membership[e[1]]:
			g.es[i]["weight"] = 3
		else:
			g.es[i]["weight"] = 1
		i += 1
	pos = net_file.find("out.")
	net = "results3/" + net_file[pos+4:]
	f = open(net + '_walktrap_' + '.dot', 'w+')
	print c.modularity
	g.write_dot(f)
	f.close()