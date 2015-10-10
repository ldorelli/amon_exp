import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def degree_histogram(data, b):
	n, bins, patches = plt.hist(data, bins=b, normed=1, log=True, alpha=0.3, color='green')

	xpos = []
	for i in range(0, len(bins)-1):
		xpos.append((bins[i]+bins[i+1])*0.5)

	plt.title('Degree Distribution')
	plt.xlabel('Degree')
	plt.ylabel('Probability')
	plt.plot(xpos, n)


	cumulative = []
	c = 0
	for i in range(0, len(n)):
		c += n[len(n) - 1 - i]
		cumulative.insert(0, c)

	plt.yscale('log')
	plt.ylabel('Probability')
	plt.xlabel('Degree')
	l1, = plt.plot(xpos, n, color='blue', label='non cumulative')
	l2, = plt.plot(xpos, cumulative, color='red', label='cumulative')
	plt.legend(handles=[l1, l2])