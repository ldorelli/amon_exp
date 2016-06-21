# -*- coding: utf-8 -*-
import amon
import amon_analytics as an
import sys
import numpy
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math

current_palette = sns.color_palette()
sns.set_style(style='white')


g = amon.Graph()
g.load_directed ('../raw/s1/netw2')
filename = 'netw2'
f = open('../raw/s1/' + filename, 'r')

print 'Loaded'
in_deg = []
out_deg = []
X = {}

K = g.node_keys()
for k in K:
    I = g.in_degree (k)
    J = g.out_degree (k)
    in_deg.append (g.in_degree(k))
    out_deg.append (g.out_degree(k))
    if I <= 150 and J <= 1000:
        if (I, J) not in X:
            X[(I, J)] = 0
        X[(I, J)] += 1


plt.close()
fig = plt.figure()
ax = fig.add_subplot(111)
Y = {}
lo = 1e9
hi = 0
for x in X:
    tam = X[x]
    lo = min (lo, math.log(tam))
    hi = max (hi, math.log(tam))
    if tam not in Y:
        Y[tam] = []
        Y[tam].append ([])
        Y[tam].append ([])
    Y[tam][0].append ( x[0] )
    Y[tam][1].append ( x[1] )

for t in Y:
    sz = math.log(t)/float(hi - lo) * 50
    ax.scatter(Y[t][0], Y[t][1],  facecolors='black', edgecolors='black', s=30, alpha=0.4)
ax.set_xlabel(u'Grau de Entrada', size=15)
ax.set_ylabel(u'Grau de Saída', size=15)
plt.grid (axis='x',color='grey', linestyle='--', lw=0.5, alpha=0.5)
plt.grid (axis='y',color='grey', linestyle='--', lw=0.5, alpha=0.5)
plt.savefig('../figs/evolution/chara/inout.pdf')

plt.close()
an.degree_histogram (in_deg,  True, True, True, 'Grau de Entrada')
plt.savefig('../figs/evolution/chara/in.pdf')

plt.close()
an.degree_histogram (out_deg,  True, True, True, u'Grau de Saida')
plt.savefig('../figs/evolution/chara/out.pdf')
