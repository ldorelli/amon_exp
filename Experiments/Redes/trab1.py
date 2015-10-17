#!/usr/bin/python
import amon
import sys
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import amon_analysis 
import os

net_file = sys.argv[1]

g = amon.Graph()
g.load_undirected(net_file)

cmps = g.connected_components()


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

big = g.filter_nodes(filt)

clust = []
degs = []
for i in range(0, big.nodes_qty()):
	degs.append(len(big.adjacency(i)))
	cc = big.local_clustering(i)
	clust.append(cc)

# Display the degree histogram
amon_analysis.degree_histogram(degs, 300)

# Get the shortest paths (max + avg)
diam = 0.0
avg_path = 0
den = 0.0
eff = 0.0
for i in range(0, big.nodes_qty()):
	dst = big.bfs(i)
	for j in dst:
		if j == i:
			continue
		diam = max(diam, dst[j])
		avg_path += dst[j]
		eff += 1/dst[j]
		den += 1
eff /= den
avg_path /= den

pos = net_file.find("out.")
net = "results/" + net_file[pos+4:]
net_n = "results/" + net_file[pos+4:]  + "_degree.png"
# print net_n
plt.tight_layout()
plt.savefig(net_n, dpi=200)
# plt.show()



print  ' & ', round(big.average_degree(), 3), ' & ', round(stats.moment(degs, 2), 3), ' & ', round(stats.entropy(degs), 3), round(np.average(clust), 3), ' & ', round(big.global_cc(), 3), ' & ',  round(avg_path, 3), ' & ', round(diam, 3), ' & ' , round(eff, 4)

s = big.as_dot(False)
f = open(net + '.dot', 'w+')
f.write(s)
f.close()

# os.system("./gen.sh " + net)
