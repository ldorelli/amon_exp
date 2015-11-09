#!/usr/bin/python
import amon
import sys
from sys import stdout
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import amon_analytics as an 
import os

G = []
f = []

for net_file in sys.argv[1:]:
	g = amon.Graph()
	g.load_undirected(net_file)
	G.append(g)

	pos = net_file.find("out.")
	net = "results/" + net_file[pos+4:]
	f.append(net)

colors = ['blue', 'red', 'black', 'green']
markers = ['.', '.', '.', '.']
names = [ 'airport', 'friendship', 'email', 'internet']

# Get largest component
for i in range(0, len(G)):
	cmps = G[i].connected_components()
	cnt = {}
	for x in cmps:
		if cmps[x] not in cnt:
			cnt[cmps[x]] = 0
		cnt[cmps[x]] += 1
	bst = -1
	for x in cnt:
		if bst == -1:
			bst = x
		elif cnt[x] > cnt[bst]:
			bst = x
	filt = []
	for x in cmps:
		if cmps[x] == bst:
			filt.append(x)
	G[i] = G[i]	.filter_nodes(filt)

# GRAU
# plt.close()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# for i in range(0, len(f)):
# 	d = []
# 	for x in G[i].node_keys():
# 		d.append(G[i].out_degree(x))
# 	dist = an.cumul(d)
# 	x = []
# 	y = []
# 	for e in sorted(dist):
# 		x.append(e)
# 		y.append(dist[e])	
# 	# ax.scatter(x, y, marker=markers[i], label=names[i], facecolors='none', edgecolors=colors[i], s=16.0)
# 	ax.plot(x, y, marker=markers[i], linestyle='--', color=colors[i], label=names[i])
	
# handles, labels = ax.get_legend_handles_labels()
# ax.set_xscale('log')
# ax.set_yticks((0.01, 0.1, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0))
# ax.set_ylim(0.03, 1.0)
# ax.set_ylabel('P($d \leq D$)', size=15)
# ax.set_xlabel('Degree (D)', size=15)
# ax.legend(handles, labels, loc=1	)
# plt.savefig('results_2/degrees.pdf')

# CLOSENESS

plt.close()
fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(0, len(f)):
	print names[i]
	d = []
	keys = G[i].node_keys()
	for x in G[i].node_keys():
		dd = G[i].bfs(x)
		r = 0.0
		for v in dd:
			if v != x:
				r += 1.0/float(dd[v])
		d.append(r/float(G[i].nodes_qty()-1))
	dr = an.cumul(d)
	x = []
	y = []
	for e in sorted(dr):
		x.append(e)
		y.append(dr[e])	
	ax.plot(x, y, linestyle='-', color=colors[i], label=names[i])
	# ax.scatter(x, y, marker=markers[i], label=names[i], facecolors='none', edgecolors=colors[i], s=16.0)

handles, labels = ax.get_legend_handles_labels()
ax.set_ylabel('P($c \leq C$)', size=15)
ax.set_xlabel('Closeness Centrality (C)', size=15)
# ax.set_yscale('log')
# ax.set_xlim(0.002, 0.025)
ax.set_ylim(0.1, 1.0)
ax.set_yticks([0.1, 0.3, 0.4, 1.0])
ax.legend(handles, labels, loc=4)
plt.savefig('results_2/closeness.pdf')

# BETWEENNESS
# 
# plt.close()
# fig = plt.figure()
# ax = fig.add_subplot(111)

# for i in range(0, len(f)):
# 	print names[i]
# 	v = G[i].betweenness_unw()
# 	d = []
# 	for dd in v:
# 		d.append(v[dd])
# 	dr = an.cumul(d)
# 	x = []
# 	y = []
# 	for e in sorted(dr):
# 		x.append(e)
# 		y.append(dr[e])	
# 	ax.plot(x, y, linestyle='-', color=colors[i], label=names[i])

# handles, labels = ax.get_legend_handles_labels()
# ax.set_yscale('log')
# ax.set_ylabel('P($c \leq B$)', size=15)
# ax.set_xlabel('Betweenness Centrality (B)', size=15)
# ax.set_ylim(0.1, 1.0)
# ax.set_xlim(0.0, 0.01)
# ax.legend(handles, labels, loc=4)
# plt.savefig('results_2/betweenness.pdf')

# EIGENVECTOR
# 
# plt.close()
# fig = plt.figure()
# ax = fig.add_subplot(111)

# for i in range(0, len(f)):
# 	print names[i]
# 	v = G[i].eigenvector_centrality(1000)
# 	d = []
# 	for dd in v:
# 		d.append(v[dd])
# 	dr = an.cumul(d)
# 	x = []
# 	y = []
# 	for e in sorted(dr):
# 		x.append(e)
# 		y.append(dr[e])	
# 	# ax.scatter(x, y, marker=markers[i], label=names[i], facecolors='none', edgecolors=colors[i], s=4.0)
# 	ax.plot(x, y, linestyle='-',   color=colors[i], label=names[i])

# handles, labels = ax.get_legend_handles_labels()
# ax.set_yscale('log')
# ax.set_ylabel('P($c \leq E$)', size=15)
# ax.set_xlabel('Eigenvector Centrality (E)', size=15)
# ax.set_ylim(0.1, 1.0)
# ax.set_xlim(0.0, 0.006)
# ax.legend(handles, labels, loc=4)
# plt.savefig('results_2/eigenvector.pdf')
# 

# Scatterplots - CORRELACAO
# 
# Degree x Betweenness
# plt.close()
# fig = plt.figure()
# ax = fig.add_subplot(111)

# for i in range(0, len(f)):
# 	print names[i]
# 	v = G[i].betweenness_unw()
# 	x = []
# 	y = []
# 	for n in v:
# 		x.append(G[i].out_degree(n))
# 		y.append(v[n])
# 	c = stats.pearsonr(x, y)
# 	print c
# 	L = names[i] + ' $(' + str(round(c[0], 2)) + ')$'
# 	ax.scatter(x, y, marker='o', label=L, facecolors='none', edgecolors=colors[i], s=4.0)


# # ax.set_yscale('log')
# ax.set_ylim(0.0, 0.08)
# ax.set_xlim(0, 300)
# handles, labels = ax.get_legend_handles_labels()
# ax.set_ylabel('Betweenness Centrality', size=15)
# ax.set_xlabel('Degree', size=15)
# ax.legend(handles, labels, loc=1)
# plt.savefig('results_2/deg_betwee.pdf')


# Eigenvector x Closeness
plt.close()
fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(0, len(f)):
	print names[i]
	v = G[i].eigenvector_centrality(1000)
	d = {}
	keys = G[i].node_keys()
	for x in G[i].node_keys():
		dd = G[i].bfs(x)
		r = 0.0
		for j in dd:
			if j != x:
				r += 1/float(dd[j])
		d[x] = r/float(G[i].nodes_qty()-1)

	x = []
	y = []
	for n in v:
		x.append(v[n])
		y.append(d[n])

	c = stats.pearsonr(x, y)
	L = names[i] + ' $(' + str(round(c[0], 2)) + ')$'
	ax.scatter(x, y, marker='o', label=L, facecolors='none', edgecolors=colors[i], s=4.0)

# ax.set_yscale('log')
# ax.set_ylim(0.0, 0.08)
ax.set_xlim(0, 0.012)
handles, labels = ax.get_legend_handles_labels()
ax.set_ylabel('Closeness Centrality', size=15)
ax.set_xlabel('Eigenvector Centrality', size=15)
ax.legend(handles, labels, loc=4)
plt.savefig('results_2/eigen_close.pdf')