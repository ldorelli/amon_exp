#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import amon
import amon_analytics as an
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import amon_analytics as an
import networkx as nx
import matplotlib as mpl
import sys

mpl.rcParams['font.family'] = 'Arial'

f = open('../hashtags2', 'r')

print 'Loading hashtags'
l = f.readline()
f.close()
tags = json.loads(l)

f = open('../hashtags_pl', 'w+')

for tag in tags:
    tags[tag] = { 'name' : tag, 'values' : tags[tag] }
    f.write ( json.dumps(tags[tag]) + '\n' )
f.close()


