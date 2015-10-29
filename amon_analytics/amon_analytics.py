from __future__ import print_function
import numpy as np
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
from scipy import stats
import math
import random



def characterize(g, location, paths=False):

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
	b = big.node_keys()
	b = random.shuffle(b)

	for i in b:
		degs.append(len(big.adjacency(i)))
		cc = big.local_clustering(i)
		clust.append(cc)

	# Get the shortest paths (max + avg)
	diam = 0.0
	avg_path = 0
	den = 0.0
	eff = 0.0
	if paths == True:
		for x in range(0, min(len(b), 1000)):
			i = b[x]
			dst = g.bfs(i)
			for j in dst:
				if j == i:
					continue
				diam = max(diam, dst[j])
				avg_path += dst[j]
				eff += 1/dst[j]
				den += 1
		eff /= den
		avg_path /= den

	# Saves the fitted degree distribution
	l, k = power_law_fit(degs)
	

	plt.savefig(location +  "/_dfit.pdf", dpi=200)

	# Saves degree distribution
	degree_histogram(degs, True, True, True)
	plt.savefig(location +  "/_degree.pdf", dpi=200)

	#  Saves accum degree 
	degree_histogram_complementar(degs)
	plt.savefig(location +  "/_degree_compl.pdf", dpi=200)

	# Saves clustering distribution
	local_cc_acc(clust)
	plt.savefig(location +  "/_clust.pdf", dpi=200)

	# local clustering x degree
	local_cc_deg_distr(degs, clust)
	plt.savefig(location +  "/_cc_deg.pdf", dpi=200)

	f = open(location + 'res.data', 'w+')
	# Prints the table 
	print (' & ', round(big.average_degree(), 3), ' & ', round(stats.moment(degs, 2), 3), ' & ', round(stats.entropy(degs), 3), ' & ', round(np.average(clust), 3), ' & ', round(big.global_cc(), 3), ' & ',  round(avg_path, 3), ' & ', round(diam, 3), ' & ' , round(eff, 4), ' \\\\hline', file=f)
	print (l, k, file=f)
	f.close()

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
		if k != 0:
			my = min(my, data[k])
		y.append(data[k])

	for k in sorted(fit):
		xf.append(k)
		yf.append(fit[k])

	ax.set_xlabel(r'Degree $ (k)$', size=25)
	ax.set_ylabel(r'$P (k \leq K)$', size=25)

	ax.plot(xf, yf, color='red', label='Fitted', linestyle='--')
	if cumul:
		ax.plot(x, y, color='black', label='Original', drawstyle='steps')	
	else:
		ax.scatter(x, y, marker='o', label='Original', facecolors='none', edgecolors='black', s=16.0)		
	handles, labels = ax.get_legend_handles_labels()
	print ('=============== ', my)
	# ax.set_yscale('log')
	ax.set_xscale('log')
	ax.set_xlim(kmin, mx)
	ax.set_ylim(my, 1.0)
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

	for kmi in range(1, min(40, mx/2)):
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


