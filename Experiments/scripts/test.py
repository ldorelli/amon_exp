import networkx as nx

g = nx.Graph()
g.add_node(0)
g.add_node(1)
g.add_node(2)
g.add_node(3)
g.add_node(4)
g.add_node(5)
g.add_node(6)
g.add_node(7)
g.add_node(8)
g.add_node(9)

g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(0, 2)
g.add_edge(2, 4)
g.add_edge(4, 5)
g.add_edge(3, 8)
g.add_edge(8, 9)

print nx.average_clustering(g)
