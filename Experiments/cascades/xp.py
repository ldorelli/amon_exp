import amon
import amon_analytics as an
import sys

t = amon.TweetLoader()

t.load('tweets', 1.0, amon.TweetNetType.mention)

g = t.get_social_network()

# an.characterize(g, 'results/1/')

h = t.get_hashtags()
i = 0
for x in h:
	
	i += 1
	psz = t.get_activations_size(x)
	# Ignore really small cascades
	if psz < 500:
		continue
	p = t.get_hashtag_activations(x)
	sys.stderr.write(str(i/float(len(h))) + '\n')
	# Run the cascade model
	cm = amon.CascadeModel(g)
	cm.run_from_record(p)
	c = cm.cascades()
	innovators = cm.innovators()
	ea = cm.early_adopters()
	T = cm.get_estimated_thresholds()
	d = cm.get_reach()
	r = c.nodes_qty()/float(len(p))

	cc = c.connected_components()
	cn = {}
	for z in cc:
		cn[cc[z]] = 1
	if r < 0.1:
		continue
	# N. Shares, Qt de ns da rede, Qt de ns da cascata, razao, conectados
	print '#Shares ', len(p), g.nodes_qty(), c.nodes_qty(), r, len(cn)
	# Razao da cascata pra rede
	print 'Hashtag: ', x, '{0:.8f}'.format(c.nodes_qty()/float(g.nodes_qty()))
	# Innovators, ratio de innovators, depth, ratio de early adopters
	print 'Innovators: ', len(innovators), '{0:.8f}'.format(len(innovators)/float(len(p))), d
	z = 0
	for x in T:
		print g.out_degree(x), T[x],
	print '\n',
	print '============================'

print 'Nodes ', g.nodes_qty()
print 'Edges ', g.edges_qty()

# print g.as_dot(True)
# lfd0rell8i
