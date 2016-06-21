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
import seaborn as sns
import pandas as pd

def get_time (date):
    x = date.split(' ')
    mon = {}
    mon['Jan'] = 0
    mon['Feb'] = 1
    mon['Mar'] = 2
    mon['Apr'] = 3
    mon['May'] = 4
    mon['June'] = 5
    mon['July'] = 6
    mon['Aug'] = 7
    mon['Sept'] = 8
    mon['Oct'] = 9
    mon['Nov'] = 10
    mon['Dec'] = 11
    days = [ 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
    seconds = [ 0 ]
    for i in range (1, len(days)):
        seconds.append ( seconds[i-1] + days[i-1] * 24 * 60 * 60 )
    res = mon[x[1]] * seconds[mon[x[1]]]
    res = res + int(x[2]) * 24 * 60 * 60
    hms = x[3].split(':')
    res += int(hms[0])*60*60 + int(hms[1])*60 + int(hms[2])
    return float(res)



current_palette = sns.color_palette()

B = {}
for i in range (0, 20):
    f = open('./BET/Output/output'+str(i), 'r')
    for line in f:
        x = line.split(' ')
        if len(x) != 2:
            continue
        x[0] = int(x[0])
        if int(x[0]) in B:
            B[x[0]] += float(x[1])
        else:
            B[x[0]] = float(x[1])

g = amon.Graph()
g.load_directed('../raw/s1/netw2')
for x in B:
    B[x] /= float(g.nodes_qty() * (g.nodes_qty() - 1))

print 'Loaded everything'
X = []
Y = []
for x in B:
    if g.out_degree(x) < 5000:
        Y.append(B[x])
        X.append(g.out_degree(x))


# f = open('../hashtags_pl')

# for line in f:
#     tag = json.loads(line)
#     if (len(tag['values'])) < 1000:
#         continue
#     app = {}
#     for t in tag['values']:
#         # print int(t['user'])
#         if t['user'] in B:
#             if B[t['user']] != 0:
#                 if t['user'] in app:
#                     continue
#                 app[t['user']] = 1
#                 Y.append (B[t['user']])
#                 # print X[-1], Y[-1]
#                 ctime = get_time(t['date'])
#                 c0 = get_time(tag['values'][0]['date'])
#                 cN = get_time(tag['values'][-1]['date'])
#                 X.append ( (ctime - c0) / (cN - c0) )


# 0,01 0,05 0,1 0,5 1
# plt.imshow (m,  interpolation='none', extent=[0, 1.0, 1e-40, 1.0], cmap=cm.Purples)
df = pd.DataFrame()
df['Degree'] = X
df['Betweenness'] = Y

plt.scatter (X, Y, alpha=0.2, s=4)
plt.ylim ([1e-18, 1e-2 ])
# plt.yticks (lins)
plt.yscale('log')
# plt.colorbar()
plt.show()
# plt.savefig('centrality_by_time.png')
