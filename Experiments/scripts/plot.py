#!/usr/bin/python
import numpy as npp
import matplotlib.pyplot as plt
import sys

# read file
file = open(sys.argv[1], 'r')

v = []
for line in file:
	v.append(float(line))
plt.plot(v, '-')
plt.show()
