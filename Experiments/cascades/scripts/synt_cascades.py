import amon
import amon_analytics
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import random
from matplotlib.gridspec import GridSpec
# import matplotlib.cm as cm
from scipy.stats.stats import pearsonr
import seaborn as sns

# Write the curve for the cascade
def write_curve (time_data, file, N):
    x = []
    y = []
    cnt = {}
    for i in time_data:
        if i not in cnt:
            cnt[i] = 1
        else:
            cnt[i] += 1

    tot = 0
    for t in cnt:
        x.append (t)
        tot += cnt[t]
        y.append (tot/float(N) * 100.0)
    if file == '../figs/time_curves/BeFoUr.png':
        print x, y

    x = sorted (x)
    y = sorted (y)
    print 'Plotting ' + file
    plt.clf()
    plt.plot (x, y, marker='.')
    plt.ylabel ('Cascade Size (% from ' + str(N) + ' users)')
    plt.xlabel ('Time (hours)')

    plt.show()
    # plt.savefig (file)

# Sample with degree as weight
def degree_sample (g, n = 100):
    x = []
    for key in g.node_keys():
        x.append ( ( key, g.out_degree (key) ) )

    s = []
    tot = 0
    for v, w in x:
        tot += w
        s.append ( (tot, v) )

    res = []
    for r in range (0, n):
        who = random.randint (0, tot)
        if who < s[0][0]:
            res.append (s[0][1])
        else:
            lo = 0
            hi = len(s)-1
            while lo != hi:
                mi = (hi + lo)/2
                if s[mi][0] >= who:
                    hi = mi
                else:
                    lo = mi + 1
            res.append (s[lo][1])

    return res


generator = amon.NetworkGen()

# Generate a random directed graph with <k> 0.005 * 10000
#g = generator.drandomnet(10000, 0.002)
g = amon.Graph()
print 'Loading network...'
g.load_directed('../netw')
print 'Network loaded!! ;)'

print g.nodes_qty(), g.edges_qty()

# Get a random cascade from this network

print 'Running simulation...'
c = amon.NETCascadeModel(g, 0.01, 200, 0.1, 0.01);

# Seeds don't make a difference if process doesn't need the network
s = 10
# f = random.sample(range(g.nodes_qty()), s)
f = degree_sample (g, s)

for i in f:
    c.set_starter (g.node_index(i), 1)

for i in range (2, 200):
    c.step(i)

gg = c.cascades()
print gg.nodes_qty(), gg.edges_qty()

X = c.adoption_times()

write_curve (X, '', g.nodes_qty())

k = gg.as_dot(True)
f = open('a.dot', 'w+')
f.write(k)
f.close()
