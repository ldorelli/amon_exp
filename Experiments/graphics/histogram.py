#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys

f = open(sys.argv[1], 'r')

data = []
for line in f:
	for w in line.split(' '):
		if len(w):
			data.append(int(w))
plt.xlim([0, 1500])
plt.title(sys.argv[3])
plt.xlabel(sys.argv[4])
plt.ylabel(sys.argv[5])
plt.hist(data, bins=int(sys.argv[2]), log=True)
plt.show()

