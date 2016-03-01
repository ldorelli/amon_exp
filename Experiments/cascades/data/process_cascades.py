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

f = open('data_cascades', 'r')

m = {}
labels = [ "name", "density", "mprob", "avg_paths1", "ccentrality1",
	"ncentrality1", "maxdist1", "avgdist1", "avg_paths2", "ccentrality2",
	"ncentrality2", "maxdist2", "avgdist2"
]

for x in labels:
	m[x] = []

cont = True
while cont:
	for x in labels:
		v = f.readline().split()

		if len(v) == 0:
			cont = False
			break

		if x != "name":
			m[x].append ( float(v[1]) )
		else:
			m[x].append ( v[1] )


plt.clf()
plt.scatter(m["mprob"], m["avgdist1"], marker='o', facecolors='black', edgecolors='none', s=20.0, alpha=0.5)
print sp.stats.pearsonr (m["mprob"], m["avgdist1"])
# plt.ylim ([1, 100000])
# plt.ylim ([0, 10])
# plt.yscale('log')
plt.show()
