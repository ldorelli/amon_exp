import amon
import networkx as nx
import json
from termcolor import colored
import sys
import matplotlib as mpl
import matplotlib.cm as cm
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from gensim import corpora, models
import gensim

def popcnt (i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24

# -*- coding: utf-8 -*-
def loadHashtagGraph ():

    f = open ('../../raw/s1/hashtags')

    usr = {}
    hashtags = {}
    rev = []
    last = {}
    last["date"] = "-"
    last["user"] = "-"
    # All hashtags shared in the last tweet
    curr_tweet = []
    adj = {}
    idx = 0
    print colored('Loading hashtag adjacency list...', 'green')
    g = amon.Graph()
    # Go
    for line in f:
        x = json.loads(line)

        if x['name'] not in usr:
            usr[x['name']] = []

        if x['name'] not in hashtags:
            g.add_node (idx)
            hashtags[x['name']] = idx
            adj[idx] = []
            rev.append (x['name'])
            idx += 1

        curv = { 'date' : x['date'], 'user' : x['user'] }
        usr[x['name']].append(int(x['user']))

        if curv == last:
            if x ['name'] not in hashtags:
                print x['name']
            curr_tweet.append (x['name'])
        else:
            for h1 in curr_tweet:
                for h2 in curr_tweet:
                    if h1 != h2:
                        adj[hashtags[h1]].append (hashtags[h2])
            curr_tweet[:] = []
            curr_tweet.append(x['name'])
        last = curv

    print colored('Done generating adj.list.', 'green')
    print colored('Generating graph...', 'blue')
    for x in adj:
        S = {}
        for y in adj[x]:
            if y not in S:
                S[y] = 1
            else:
                S[y] = 1
        for y in S:
            if x < y:
                g.add_edge (x, y, S[y])
    print colored('Done generating graph', 'green')
    return rev, g, usr

def jaccard (A, B):
    return len ( set(A) & set(B))/float(len (set(A) | set(B)))

def loadUserGraphFromTopics (communities, g):
    f = open ('../../raw/s1/hashtags')
    print colored ('Loading topics', 'blue')

    hashtags_by_user = {}
    users_by_hashtag = {}

    res = amon.Graph()

    rev = []
    hashtags = {}
    idx = 0
    usr = {}
    for line in f:
        x = json.loads(line)

        if x['name'] not in hashtags:
            hashtags[x['name']] = idx
            idx += 1
            rev.append(x['name'])

        H = hashtags[x['name']]
        H = int(communities[H])

        if x['user'] not in hashtags_by_user:
            hashtags_by_user[x['user']] = []

        hashtags_by_user[x['user']].append (H)
        if H not in users_by_hashtag:
            users_by_hashtag[H] = []
        users_by_hashtag[H].append (x['user'])

    print colored ('Done pre generating values, calculating graph now', 'blue')

    K = g.node_keys()
    K =  set(K)
    for u in hashtags_by_user:
        res.add_node (u)
        if u in K:
            d = g.out_degree (u)
            c = {}
            for t in hashtags_by_user[u]:
                if len (users_by_hashtag[t]) > 4000:
                    continue
                for u2 in users_by_hashtag[t]:
                    if u2 == u:
                        continue
                    c[u2] = 1

        candidates = []
        for x in c:
            candidates.append ( ( -jaccard (hashtags_by_user[u], hashtags_by_user[x]), x )  )

        candidates = sorted (candidates)
        R = min (d, len (candidates))
        for z in range (0, R):
            res.add_dedge (u, candidates[z][1])

    return res

def do_lda():
    f = open ('../../raw/s1/hashtags')

    lists = []
    usr = {}
    hashtags = {}
    rev = []
    last = {}
    last["date"] = "-"
    last["user"] = "-"
    # All hashtags shared in the last tweet
    curr_tweet = []
    idx = 0
    print colored('Loading corpus...', 'blue')
    # Go
    for line in f:
        x = json.loads(line)

        if x['name'] not in hashtags:
            hashtags[x['name']] = idx
            rev.append (x['name'])
            idx += 1

        curv = { 'date' : x['date'], 'user' : x['user'] }
        if curv == last:
            if x ['name'] not in hashtags:
                print x['name']
            curr_tweet.append (x['name'])
        else:
            lists.append (curr_tweet)
            curr_tweet = [ x['name'] ]

        last = curv

    print colored('Done loading corpus', 'green')

    print colored('Loading dictionary', 'blue')
    dictionary = corpora.Dictionary(lists)
    corpus = [dictionary.doc2bow(l) for l in lists]
    print colored('Done loading dictionary', 'green')

    print colored('Calculating LDA...', 'blue')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=50, id2word = dictionary, passes=10)
    print colored('Done calculating LDA...', 'green')


if __name__ == "__main__":
    # Sad
    # do_lda()
    H, g, usr = loadHashtagGraph()
    print colored('Calculating communities...', 'blue')
    C = g.communities()

    print colored('Done generating communities', 'green')

    print colored('Nodes: ', 'magenta'), g.nodes_qty()
    print colored('Edges: ', 'magenta'), g.edges_qty()

    S = {}
    big = 0
    R = {}
    for x in C:
        if x < 0:
            continue
        com = int(C[x])
        if com not in S:
            S[com] = 1
        else:
            S[com] += 1
            big = max (big, S[com])
        if com not in R:
            R[com] = []
        R[com].append (H[x])

    print colored('Communities ', 'magenta'), len(S)
    print colored('Big com ', 'magenta'), big

    # for x in R:
    #     if len (R[x]) == 1:
    #         continue
    #     print colored ('COM ' + str(x), 'magenta')
    #     for h in R[x]:
    #         print h.encode('utf-8'),
    #     print '\n'
    #
    # L = g.as_dot (False)
    # f = open ('hashtags.dot', 'w')
    # f.write (L)
    # f.close()

    print colored ('Loading users network', 'blue')
    # hf and g
    nf = amon.Graph()
    nf.load_directed ('../../raw/s1/netw2')
    print colored ('Loaded users network', 'green')

    g = loadUserGraphFromTopics (C, nf)

    print nf.jaccard_index(g)
    print colored ('All networks loaded', 'green')
