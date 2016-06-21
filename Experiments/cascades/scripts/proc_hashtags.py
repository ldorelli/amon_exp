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

f = open('../raw/s1/hashtags', 'r')

tags = {}
for line  in f:
    t = json.loads(line)
    if t['name'] not in tags:
        tags[t['name']] = []

    tags[t['name']].append ( { 'date' : t['date'], 'user' : t['user'] })

for tag in tags:
    t = { 'name': tag, 'values' : tags[tag] }
    print json.dumps (t)
f.close()
