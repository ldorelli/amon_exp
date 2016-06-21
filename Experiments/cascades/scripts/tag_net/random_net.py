import amon
import networkx as nx
import json
from termcolor import colored
import sys
import matplotlib as mpl
import matplotlib.cm as cm
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print colored ('Loading...', 'blue')

J = []
for i in range (0, 20):
    f = open ('random_points/output' + str(i))
    X = f.readline().split()
    for u in X:
        J.append (float(u))

sns.distplot (J, bins=250, norm_hist=True, hist=True, color='Black')
plt.xlim ([0, 1e-6])
plt.xticks ( [0, 1e-7, 5e-7, 1e-6], ['0', '$10^{-7}$', '$5 * 10^{-7}$', '$10^{-6}$'] )

plt.show()
