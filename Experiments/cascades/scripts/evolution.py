# -*- coding: utf-8 -*-
import amon
import amon_analytics as an
import sys
import numpy
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# current_palette = sns.color_palette()
sns.set_style(style='white')

g = amon.Graph()

x = []
y = []
xd = []
yd = []
cc = []
ma = []
big_cc = []

vis = {}

filename = 'netw2'
f = open('../raw/s1/' + filename, 'r')

for line in f:
	if not line[0].isdigit():
		continue
	l = line.split(' ')
	if len(l) != 2:
		continue
	a = int(l[0])
	b = int(l[1])

	if (a, b) not in vis:
		vis[(a, b)] = 1
		g.add_dedge(a, b)

	if g.edges_qty()%50000 == 0:
		xd.append(g.edges_qty())
		yd.append(g.average_degree())
		x.append(g.edges_qty())
		y.append(g.global_cc())
		ma.append(g.mix_assortativity())

f.close()

print g.edges_qty(), g.global_cc()

plt.close()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x, y, alpha=1, facecolors='black', edgecolors='none', s=3.0)
ax.set_ylim([0, 0.05])
ax.set_xlabel('#Arestas', size=15)
ax.set_ylabel('Coeficiente de Clustering', size=15)
plt.grid (axis='x',color='grey', linestyle='--', lw=0.5, alpha=0.5)
plt.savefig('../figs/evolution/clustering_' + filename + '.pdf')



plt.close()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x, ma, alpha=1, facecolors='black', edgecolors='none', s=3.0)
ax.set_xlabel('#Arestas', size=15)
ax.set_ylabel('Mixing Assortativity', size=15)
plt.grid (axis='x',color='grey', linestyle='--', lw=0.5, alpha=0.5)
plt.savefig('../figs/evolution/ma_' + filename + '.pdf')

plt.close()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(xd, yd, alpha=1, facecolors='black', edgecolors='none', s=3.0)
ax.set_xlabel('#Arestas', size=15)
ax.set_ylabel(u'Grau Médio', size=15)
plt.grid (axis='x',color='grey', linestyle='--', lw=0.5, alpha=0.5)
plt.savefig('../figs/evolution/degree_' + filename + '.pdf')

an.characterize (g, '../figs/evolution/chara')
