#! /usr/bin/env python
# -*- coding: utf-8 -*-
import csv, gensim,  numpy, re, math, tree

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)


def line2vec (line, w2v):
    stopwords_list = ['товары', 'для', 'подарки']
    stopwords = {}
    for w in stopwords_list:
        stopwords[w.decode("utf-8")] = 1
    line = re.sub(u"(?:[^а-яa-zё])", " ", line.lower())
    words = line.split(" ")
    counter = 0
    vector = numpy.zeros((1, 100))
    for word in filter(lambda  x: (x != "" and not(stopwords.has_key(x))),  words):
        if word == "" or stopwords.has_key(word):
            next
        try:
            vector = vector + w2v.word_vec(word)
            counter += 1
        except KeyError:
            next
    if counter == 0:
        return vector
    return vector / counter

def build_new_hierarchy(file, w2v):
    hierarchy = tree.Tree()
    tracker = {}
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            for level in range(1, 7):
                try:
                    dummy = tracker[str(level) + ' ' + row[level + 2]]
                except KeyError:
                    tracker[str(level) + ' ' + row[level + 2]] = 1
                    if level > 1:
                        node = tree.Node(str(level) + ' ' + row[level + 2], line2vec(row[level + 2].decode("utf-8"), w2v))
                        parent = tree.Node(str(level - 1) + ' ' + row[level + 1], line2vec(row[level + 1].decode("utf-8"), w2v))
                        hierarchy.add_node(node, parent)
                    else:
                        node = tree.Node(str(level) + ' ' + row[level + 2], line2vec(row[level + 2].decode("utf-8"), w2v))
                        hierarchy.add_node(node)
    return hierarchy

def build_hierarchy(file, w2v):
    hierarchy = {}
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            for level in range(2,7):
                try:
                    dummy = hierarchy[level]
                    try:
                        nd = dummy[row[2 + level]]
                    except KeyError:
                        hierarchy[level][row[2 + level]] = line2vec(row[2 + level].decode("utf-8"), w2v)
                except KeyError:
                    hierarchy[level] = {}
                    hierarchy[level][row[2 + level]] = line2vec(row[2 + level].decode("utf-8"), w2v)
    return hierarchy


#w2v_path = "/Users/dmitri/Documents/b2basket/all.norm-sz100-w10-cb0-it1-min100.w2v"
#w2v = gensim.models.KeyedVectors.load_word2vec_format(w2v_path, binary=True, unicode_errors='ignore')
#hierarchy = build_hierarchy('/Users/dmitri/Documents/b2basket/good_items.scv', w2v)

#for level in hierarchy.keys():
#    for cat in hierarchy[level].keys():
#        print cat
