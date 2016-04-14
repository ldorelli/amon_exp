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
#g = generator.drandomnet(10000, 0.002)
g = amon.Graph()
print 'Loading network...'
g.load_directed('../netw')
print 'Network loaded!! ;)'


# Get a random cascade from this network
c = amon.CascadeModel(g, 0.01, 50, 0.0002);

s = 100
f = random.sample(range(g.nodes_qty()), s)

for x in f:
    c.set_starter(x, 0)

for i in range (0, 500):
    c.step(i)

gg = c.cascades()
print gg.nodes_qty(), gg.edges_qty()
k = gg.as_dot(True)
f = open('a.dot', 'w+')
f.write(k)
f.close()
