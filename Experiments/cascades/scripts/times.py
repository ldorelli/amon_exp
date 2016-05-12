import math
import json
import amon
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

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


def write_histogram (time_data, file):
    print 'Histogram'
    plt.clf()
    sns.distplot (t)
    plt.savefig (file)

def write_curve (time_data, file, N, legend):
    x = []
    y = []

    cnt = {}
    for i in time_data:
        if i not in cnt:
            cnt[i] = 1
        else:
            cnt[i] += 1

    x2 = []
    l = []
    tot = 0
    k = 0
    for t in cnt:
        x.append (t)
        if k%6 == 0:
            x2.append (t)
            l.append (legend[t])
        k += 1
        tot += cnt[t]
        y.append (tot/float(N) * 100.0)
    if file == '../figs/time_curves/BeFoUr.png':
        print x, y

    x = sorted (x)
    y = sorted (y)
    print 'Plotting ' + file
    plt.clf()
    plt.plot (x, y, marker='o',  markersize=2.5)
    plt.xticks (x2, l, rotation=45)
    plt.ylabel ('Cascade Size (% from ' + str(N) + ' users)')
    plt.xlabel ('Time (hours)')
    plt.savefig (file)


current_palette = sns.color_palette()
mpl.rcParams['xtick.labelsize'] = 7

print 'Loading Network...'
g = amon.Graph()
g.load_directed ('../raw/s1/netw2')
N = g.nodes_qty()
f = open('../raw/s1/hashtags_pl', 'r')

print 'Starting...'

for l in f:
    j = json.loads(l)

    if len(j['values']) < 1000:
        continue

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

    if len(use) < 1000:
        continue

    write_histogram (t, '../figs/htimes/' + j['name'] + '.png')
    write_curve (t, '../figs/time_curves/' + j['name'] + '.png', N, hours)
