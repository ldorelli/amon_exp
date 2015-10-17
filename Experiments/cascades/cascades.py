import amon
import amon_analytics
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import random
from matplotlib.gridspec import GridSpec
# import matplotlib.cm as cm
from scipy.stats.stats import pearsonr   

generator = amon.NetworkGen()

# Generate a random directed graph with <k> 0.005 * 10000
g = generator.drandomnet(1000, 0.002)
bet = g.betweenness_unw()

print 'Generated Random Network\n'


markers = [ '|', '_', 'x', '.', '1', '*', '2', '+' ]
# colors = cm.coolwarm(np.linspace(0, 1, 10))
modes = ['random' 	]
for mode in modes:
	ini = 0
	iters = 50
	threshold = 0.15
	T = 0.4

	fig, ax = plt.subplots()
	X = []
	Y = []
	while threshold <= T:	
		resx = []
		resy = []
		tetas = []
		md = 0.0
		csz = 0.0
		for k in range(0, iters):
			cm = amon.CascadeModel(g, 0.01, threshold, mode)
			while True:
				r = cm.step()
				if r == True:
					break
			
			C = cm.cascades()
			inn = cm.innovators()
			ear = cm.early_adopters()
			degs = []
			for x in ear:
				degs.append(bet[x])
			mdeg = np.average(degs)
			md += mdeg
			csz += float(C.nodes_qty())/float(g.nodes_qty())
			resx.append(mdeg)
			# resy.append(cm.max_reach())
			resy.append(float(C.nodes_qty())/float(g.nodes_qty()))
		# resx.append(md/iters)
		# resy.append(csz/iters)
		# tetas.append(threshold)
		threshold += 0.05
		ax.scatter(resx, resy, label=str(threshold), color='b', marker=markers[ini])
		ini += 1

		X += resx
		Y += resy

	print np.corrcoef(X, Y)
	# plt.yscale('log')
	plt.legend(loc='upper left')
	plt.savefig('figs/res'  + mode + '.jpg')
	