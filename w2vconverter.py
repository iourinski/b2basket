#! /usr/bin/env python
# -*- coding: utf-8 -*-

import build_ontology, tree, re

def match_cat(hierarchy, w2v, category):
    vec = build_ontology.line2vec(category, w2v)
    cos = 0
    res = ""
    l = 1
    for level in hierarchy.keys():
        for lev_cat in hierarchy[level].keys():
            match = build_ontology.cosine_similarity(vec[0], hierarchy[level][lev_cat][0])
            if match > cos:
                cos = match
                res = lev_cat
                l = level
    return res, cos, l

def match_tree_category(categories, hierarchy, w2v):
    nodes = hierarchy.get_nodes("^1")
    res = []
    for cat in categories:
        vec = build_ontology.line2vec(cat, w2v)
        cos = 0
        r = ""
        for node in nodes:
            match = build_ontology.cosine_similarity(vec[0], node.vector[0])
            if match > cos:
                cos = match
                r = node.identifier
        res.append(r)
        nodes = node.children
    return res

def match_tree_category_loose(categories, hierarchy, w2v):
    nodes = hierarchy.get_nodes("^1")
    res = []
    for node in nodes:
        loc_match = [node.identifier]
        for cat in categories:
            vec = build_ontology.line2vec(cat, w2v)
            cos = 0
            r = ""
            dummy = node

            for n in dummy.children:
                match = build_ontology.cosine_similarity(vec[0], n.vector[0])
                if match > cos:
                    cos = match
                    r = n.identifier
                    dummy = n
            loc_match.append((r, match))

        res.append(loc_match)
    return res