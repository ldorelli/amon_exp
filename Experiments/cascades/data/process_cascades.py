#!/usr/bin/env python
# -*- coding: utf-8 -*-
from matplotlib.colors import LogNorm
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
import matplotlib.cm as cm
import seaborn as sns
import pandas as pd

f = open('data_cascades3', 'r')

m = {}
labels = [ "name", "density", "timei",  "mprob", "dpaths", "avg_paths1", "ccentrality1",
	"ncentrality1", "maxdist1", "avgdist1" ]

names = {}
names['dpaths'] = 'Number of Disjoint Paths'
names['timei'] = 'STW (70%)'
names['name'] = 'Hashtag Name'
names['density'] = 'Density'
names['mprob'] = 'P (X | A)'
names['avg_paths1'] = 'Average Number of Paths to Node'
names['ccentrality1'] = 'Cascade Centrality'
names['ncentrality1'] = 'Network Centrality of Cascade'
names['maxdist1'] = 'Maximum Cascade Reach'
names['avgdist1'] = 'Average Distance'

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

current_palette = sns.color_palette()

while True:
	print 'Enter command:'
	x = raw_input()

	if x == "stop":
		print 'Leaving... bye ;)'
		break
	else:
		v = x.split(' ')
		df = pd.DataFrame()
		df[names[v[0]]] = m[v[0]]
		df[names[v[1]]] = m[v[1]]
		sns.jointplot (x=names[v[0]], y=names[v[1]], data=df, alpha=0.5)
		plt.savefig ('../figs/cascade_grap/' + v[2])
		print 'Saved fig ' + v[2]
