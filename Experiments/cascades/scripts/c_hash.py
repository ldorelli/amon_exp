# -*- coding: utf-8 -*-
import math
import json
import amon
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import amon_analytics as an

sns.set_style(style='white')
# Mon Mar 14 05:29:54 +0000 2016
def get_time (date):
    x = date.split(' ')

    mon = {}
    mon['Jan'] = 0
    mon['Feb'] = 1
    mon['Mar'] = 2
    mon['Apr'] = 3
    mon['May'] = 4
    mon['June'] = 5
    mon['July'] = 6
    mon['Aug'] = 7
    mon['Sept'] = 8
    mon['Oct'] = 9
    mon['Nov'] = 10
    mon['Dec'] = 11

    days = [ 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

    hours = [ 0 ]
    for i in range (1, len(days)):
        hours.append ( hours[i-1] + days[i-1] * 24 )

    res = mon[x[1]] * hours[mon[x[1]]]
    res = res + (int(x[2])-1) * 24

    hms = x[3].split(':')
    res += int(hms[0])
    # + int(hms[1])*60 + int(hms[2])
    hstring = x[1] + ' ' + x[2] + ' ' + hms[0] + 'h'
    return res, hstring



current_palette = sns.color_palette()
mpl.rcParams['xtick.labelsize'] = 7

print 'Loading Network...'
# g = amon.Graph()
# g.load_directed ('../raw/s1/netw2')
# N = g.nodes_qty()
f = open('../raw/s1/hashtags_pl2', 'r')
print 'Starting...'

data2 = []
data = []
per = [ ]
for l in f:
    j = json.loads(l)

    # if len(j['values']) < 1000:
        # continue
    t = []
    use = {}
    hours = {}
    for x in j['values']:
        if x['user'] not in use:
            p = get_time (x['date'])
            if p[1].find("Apr 27") != -1:
                continue
            t.append (p[0])
            hours[p[0]] = p[1]
            use[x['user']] = 1

    d2 = len(use)/float(len(j['values']))
    d2 = round (d2, 3)

    data.append (len(use))
    per.append ( (-len(use), j['name']))
    if len(use) > 1:
        data2.append (d2)

per = sorted (per)
print data2
for i in range (0, 10):
    print per[i][1] + ' & ' + str(-per[i][0]) + ' \\\\ \\hline'
plt.close()
fig = plt.figure()
ax = fig.add_subplot(111)
# plt.grid (axis='x',color='grey', linestyle='--', lw=0.5, alpha=0.5)
an.degree_histogram (data, True, True, True, u'#Usuários Únicos')
# plt.grid (axis='y',color='grey', linestyle='--', lw=0.5, alpha=0.5)
plt.savefig('../figs/tags/distr.pdf')
an.degree_histogram (data2, True, True, False, u'Usuários Totais/Usuários Únicos')
plt.savefig('../figs/tags/distr2.pdf')
