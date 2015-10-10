#!/usr/bin/env python
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import sys
from matplotlib.gridspec import GridSpec

# 1: File
# 2: Title
# 3: xlabel
# 4: ylabel

f = open(sys.argv[1], 'r')

data = [ [], [] ]
for line in f:
	v = line.split(' ')
	for i in range(0, len(v)):
		data[i].append(float(v[i]))



# f = plt.figure(figsize=[100, 100])

# f, ((ax1, ax2), (ax3 , ax4)) = plt.subplots(2, 2, sharex=False,sharey=False)
# gs = GridSpec(100, 100, bottom=0.18,left=0.18,right=0.88)

# 2D histogram
plt.subplot(2, 2, 4)
# ax = f.add_subplot(gs[50:100, 50:100])
plt.title("")
plt.xlabel("Outdegree")
plt.ylabel("Depth")
plt.hist2d(data[0], data[1], bins=50, range=[[0, 100], [0, 70]], norm=LogNorm(), cmap=plt.cm.YlGnBu) 
plt.colorbar()
# ax.get_figure().colorbar(im, ax=ax)

# 1st Histogram
plt.subplot(2, 2, 2)
# ax = f.add_subplot(gs[0:45, 50:100])
n, bins, patches = plt.hist(data[0], log=True, orientation='vertical',bins=30, color=['gray'])
cm = plt.cm.YlGnBu
bin_centers = 0.5 * (bins[:-1] + bins[1:])
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))


plt.ylabel("Frequency")
plt.xlabel("Outdegree")


plt.subplot(2, 2, 3)
n, bins, patches = plt.hist(data[1], orientation='horizontal', bins=30, log=True, color=['gray'])
cm = plt.cm.YlGnBu
bin_centers = 0.5 * (bins[:-1] + bins[1:])
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
plt.xlabel("Frequency")
plt.ylabel("Depth")

# x = np.vstack((np.log(np.array(data[0]) + 1), np.log((np.array(data[1]) + 1))))
# plt.subplot(2, 2, 1)
# plt.scatter(x[0], x[1], s=5, alpha=0.05)
# plt.gca().set_yscale('log')
# plt.gca().set_xscale('log')
# cl = ax.colorbar()

print np.corrcoef(data)

plt.show()

