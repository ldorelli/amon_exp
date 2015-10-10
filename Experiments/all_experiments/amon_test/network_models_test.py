import amon
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

generator = amon.NetworkGen()
g = generator.randomnet(1000, 0.3)
degs = []
for i in range(0, g.nodes_qty()):
	degs.append( g.out_degree(i) )

plt.hist(degs)
plt.show()