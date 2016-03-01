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

f = open('centrality_cascade', 'r')

A = []
B = []

for line in f:
    x = line.split()
    A.append(float(x[0]))
    B.append(float(x[1]))

plt.scatter(A, B, facecolors='blue', edgecolors='none', s=2.5, alpha=0.5)
plt.ylim([1e-80, 1.0])
plt.yscale('log')
plt.savefig('centrality_by_time.png')

