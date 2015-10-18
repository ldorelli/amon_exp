import numpy as np
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
import math


def rng_powerlaw(xmin, a, size=1):
	nr = np.random.random(size)
	res = []
	for r in nr:
		val = math.floor( (xmin - 0.5) * ((1. - r)**(-1.0/(a-1.))) + .5)
		res.append(val)
	return res


def power_law_lambda(kmin, degs):
	s = 0.0
	for x in degs:
		s += math.log1p(float(x)/float(kmin))
	return 1.0 + float(len(degs))/s;

def distr(data):
	cnt = {}
	n = len(data)
	for x in data:
		if x not in cnt:
			cnt[x] = 0
		cnt[x] += 1
	for x in cnt:
		cnt[x] /= float(n)
	return cnt

def cumul(data):
	cnt = {}
	n = len(data)
	for x in data:
		if x not in cnt:
			cnt[x] = 0
		cnt[x] += 1

	c = 0
	for x in sorted(cnt):
		c += cnt[x]
		cnt[x] = float(c)/float(n)		
	return cnt

def plot_with_fit(data, fit, kmin, cumul=False):
	plt.clf()

	fig, ax = plt.subplots(1, 1, figsize=(8,8))

	x = []
	y = []
	xf = []
	yf = []	
	mx = 0
	my = 1
	for k in sorted(data):
		x.append(k)
		mx = max(mx, k)
		my = min(my, data[k])
		y.append(data[k])

	for k in sorted(fit):
		xf.append(k)
		yf.append(fit[k])

	# ax.set_yscale('log')
	ax.set_xscale('log')
	ax.set_xlim(kmin, mx)
	ax.set_ylim(my, 1)

	ax.set_xlabel(r'Degree $ (k)$', size=25)
	ax.set_ylabel(r'$P (k \leq K)$', size=25)

	ax.plot(xf, yf, color='red', label='Fitted', linestyle='--')
	if cumul:
		ax.plot(x, y, color='black', label='Original', drawstyle='steps')	
	else:
		ax.scatter(x, y, marker='o', label='Original', facecolors='none', edgecolors='black', s=16.0)		
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels, loc=4)

def power_law_fit(data):
	bst = 1000.0
	n = len(data)
	m = np.max(data)
	S = cumul(data)
	D = {}
	d = []
	L = 0
	KM = 0

	mx = 0
	for x in data:
		mx = max(mx, x)

	for kmi in range(1, min(10, mx/2)):
		l = power_law_lambda(kmi, data)

		ddata = rng_powerlaw(kmi, l, 5000)
		P = cumul(ddata)
		r = 0.0
		for x in S:
			if x in P:
				r = max(r, abs(S[x] - P[x]))		
		if r < bst:
			bst = r
			D = P
			L = l
			KM = kmi
			d = ddata

	plot_with_fit(S, D, KM, True)
	return L, KM


def local_cc_deg_distr(degs, clust):
	plt.clf()
	fig, ax = plt.subplots(1, figsize=(8,8))

	xv = []
	yv = []
	mdeg = 0
	for i in range(0, len(degs)):
		if clust[i] > 0.0:
			xv.append(degs[i])
			yv.append(clust[i])
			mdeg = max(mdeg, degs[i])

	ax.scatter(xv, yv, marker='o', facecolors='none', edgecolors='black', s=16.0)
	ax.plot([1, mdeg], [1.0, 0.001], linestyle='--', color='black')
	plt.xlabel('Degree $(k)$', size=25)
	plt.ylabel('Local clustering coefficient $C(k)$', size=25)
	plt.xscale('log')
	plt.yscale('log')	
	ax.set_xlim(1, mdeg + 10)
	ax.set_ylim(0.001, 1.000)
	ax.set_yticks((0.01, 0.1, 1.0))

def local_cc_acc(data):
	plt.clf()
	mxv = len(data)
	cnt = {}
	for x in data:
		if x not in cnt:
			cnt[x] = 0
		cnt[x] += 1

	dx = []
	dy = []
	C = cumul(data)
	for x in sorted(C):
		dx.append(x)
		dy.append(C[x])

	plt.plot (dx, dy, color='black',  drawstyle='steps')
	plt.xlabel('Local clustering coefficient $(c)$', size=25)
	plt.ylabel('$P(x \leq c)$', size=25)
	# plt.yscale('log')

def degree_histogram(data, logX=True, logY=True, tight=False):	
	plt.clf()
	# plt.figure()
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

	plt.ylabel('Frequency', size=25)
	plt.xlabel('Degree', size=25)
	
	plt.scatter(xpos, yvs,  marker='o', facecolors='none', edgecolors='black')
	
	if tight == True:
		plt.xlim([1, maxv])
		plt.ylim([minv, maxy])
	if logX == True:
		plt.xscale('log')
	if logY == True:
		plt.yscale('log')	

def degree_histogram_complementar(data):	
	plt.clf()
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

	minv = len(data)
	maxy = 0
	for y in yvs:
		maxy = max(maxy, y)
		minv = min(minv, y)

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
	plt.ylabel('$P (d \geq x)$', size=25)
	plt.xlabel('Degree (d)', size=25)
	plt.xlim([1, maxv])
	plt.ylim([minv, 1])
	plt.legend()
	l2, = plt.plot(xpos, yvs, color='black', label='cumulative', drawstyle='steps')
