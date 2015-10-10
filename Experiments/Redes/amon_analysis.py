import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os


def degree_histogram(data, b):	
	n, bins = np.histogram(data, bins=b, normed=1)

	plt.figure(figsize=(20, 10))

	plt.subplot(1, 2, 1)
	maxv = 0
	cnt = {}
	for x in data:
		if x not in cnt:
			cnt[x] = 0
		cnt[x] += 1

	xpos = []
	yvs = []
	for x in cnt:
		maxv = max(maxv, x)
		xpos.append(x)
		yvs.append(cnt[x])

	minv = len(data)
	maxy = 0
	for y in yvs:
		maxy = max(maxy, y)
		minv = min(minv, y)

	plt.title('Degree Distribution')
	plt.ylabel('Frequency')
	plt.xlabel('Degree')
	plt.xlim([1, maxv])
	plt.ylim([minv, maxy])
	plt.scatter(xpos, yvs, color='blue', marker='o')
	plt.xscale('log')
	plt.yscale('log')	

	plt.subplot(1, 2, 2)
	# ax2.ax1.minorticks_on()

	xpos = []
	yvs = []

	plt.title('Cumulative Distribution')
	plt.xscale('log')
	cumulative = []
	c = 0
	for i in range(0, maxv):
		x = maxv - i
		if x in cnt:
			c += cnt[x]
		yvs.insert(0, c)
		xpos.insert(0, x)

	minv = 1
	for i in range(0, len(yvs)):
		yvs[i] = float(yvs[i])/c
		minv = min(yvs[i], minv)

	plt.yscale('log')
	plt.ylabel('P (d >= x)')
	plt.xlabel('Degree (d)')
	plt.xlim([1, maxv])
	plt.ylim([minv, 1])
	plt.legend()
	l2, = plt.plot(xpos, yvs, color='blue', label='cumulative', drawstyle='steps')


