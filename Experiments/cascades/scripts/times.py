import math
import json
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import scipy

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

    seconds = [ 0 ]
    for i in range (1, len(days)):
        seconds.append ( seconds[i-1] + days[i-1] * 24 * 60 * 60 )

    res = mon[x[1]] * seconds[mon[x[1]]]
    res = res + int(x[2]) * 24 * 60 * 60

    hms = x[3].split(':')
    res += int(hms[0])*60*60 + int(hms[1])*60 + int(hms[2])

    return res

f = open('../hashtags2', 'r')
l = f.readline()

j = json.loads(l)

for tag in j:

    if len(j[tag]) < 1000:
        continue

    t = []
    for x in j[tag]:
        t.append (get_time(x['date'])/(60.0*60.0))

    bs = (t[-1]-t[0])
    plt.clf()
    sns.distplot (t, bins=bs)
    plt.savefig('../figs/htimes/' + tag + '.png')
