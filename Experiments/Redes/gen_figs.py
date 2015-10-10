import networkx as nx
import matplotlib.pyplot as plt

g = nx.Graph()

N = 6
for i in range(0, N):
	g.add_node(i + 1)

labels = {}
for x in range(0, N):
	labels[i] = str(i)

edges = [ (1, 2), (1, 3), (1, 5), (3, 4), (2, 4), (2, 6) ]
E = {}

for e in edges:
	E[e] = 1
	g.add_edge(e[0], e[1])

plt.axis('off')

pos = nx.spring_layout(g)
nx.draw_networkx_nodes(g, pos, node_color='w', node_size=1500)
nx.draw_networkx_labels(g, pos)
nx.draw_networkx_edges(g, pos)
plt.show()

print '\\begin{bmatrix}'
for i in range(0, N):
	lin = ''
	for j in range(0, N):
		if (i + 1, j + 1) in E:
			lin += '1'
		else:
			lin += '0'

		if j != N-1:
			lin += ' & '
		else:
			lin += ' \\\\ '
	print lin
print '\\end{bmatrix}'