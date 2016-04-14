#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import amon
import amon_analytics as an
import numpy as np
import scipy as sp
from matplotlib.colors import LogNorm
from scipy import stats
import matplotlib.pyplot as plt
import amon_analytics as an
import networkx as nx
import matplotlib as mpl
import matplotlib.cm as cm



f = open('centrality_cascade3', 'r')

A = []
B = []

for line in f:
    x = line.split()
    if float(x[1]) == 0 or float(x[1]) > 200:
        continue
    A.append(float(x[0]))
    B.append(float(x[1]))


plt.hist2d (A, B, bins=100, cmap=cm.Blues, norm=LogNorm())
plt.ylim([0, 200])
plt.colorbar()
plt.savefig('centrality_by_time.png')
