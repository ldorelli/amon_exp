import sys
import math
import numpy as np
from scipy import stats

f = open ('path1', 'r')

A = []
T = []

n = 0
m = 0
for line in f:
    x = line.split()
    if x[0] == x[1]:
        A.append (1.0)
        m += 1
    else:
        A.append (0.0)
    n += 1
    T.append(m/float(n))

print np.mean(A)

