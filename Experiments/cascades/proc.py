import amon
import amon_analytics as an
import matplotlib.pyplot as plt


f = open('output', 'r')

lines = []
for line in f:
	lines.append(line)

sz = []
deps = []
invs = []
t = []
i = 0
v1 = []
v2 = []
while i+2 < len(lines):
	cs = int(lines[i].split(' ')[2])
	inov = float(lines[i+2].split(' ')[3])
	dd = int(lines[i+2].split(' ')[4])
	deps.append(dd)
	invs.append(inov)
	sz.append(cs)
	if inov <= 0.6 and cs >= 2000:
		print lines[i+1].split(' ')[2], ' & ', cs, ' & ', inov, ' & ', dd, ' \\\\ \hline'
	v = lines[i+3].split(' ')
	for j in range(0, len(v)):
		if j%2 == 1:
			continue
		if j+1 >= len(v):
			break
		if float(v[j+1]) != 0:
			v1.append(float(v[j]))
			v2.append(float(v[j+1]))
	i += 5

plt.hist(invs, bins=30, color='gray')
plt.xlabel('Innovators Ratio', size=25)
plt.ylabel('Frequency', size=25)
plt.savefig('results/1/inov.pdf', dpi=200)

plt.clf()
plt.scatter(sz, invs, marker='o', label='Original', facecolors='none', edgecolors='black', s=16.0)		
plt.xlabel('#Shares', size=25)
plt.ylabel('Innovators Ratio', size=25)
plt.xscale('log')
plt.savefig('results/1/inov_sz.pdf', dpi=200)

plt.clf()
plt.scatter(deps, sz, marker='o', label='Original', facecolors='none', edgecolors='black', s=16.0)		
plt.xlabel('Depth', size=25)
plt.ylabel('Cascade Size', size=25)
plt.yscale('log')
plt.savefig('results/1/inov_dept.pdf')


plt.clf()
plt.hist(deps, bins=14, color='gray')
plt.xlabel('Depth', size=25)
plt.ylabel('Frequency', size=25)
plt.savefig('results/1/dep_hist.pdf')

plt.clf()
plt.hist(v2, bins=50, color='gray')
plt.yscale('log')
plt.savefig('results/1/threshold_degree.pdf')
