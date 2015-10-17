import amon

tl = amon.TweetLoader()
tl.load_retweet_network('tweets', 0.005)
g = tl.get_social_network()
s = g.as_dot(True)

f = open('test.dot', 'w+')
f.write(s)
f.close()


