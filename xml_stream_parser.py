#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import gensim, build_ontology, sys, getopt, w2vconverter

from w2vconverter import match_cat

def getParents(categories, id):
    if categories.has_key(id) == False:
        return list()
    else:
        if categories[id]["parentId"] == None:
            return list()
        else:
            res = getParents(categories, categories[id]["parentId"])
            res.append(categories[id]["parentId"])
            return res

def main(argv):
    benchmark = ''
    catalogue_file = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hb:c:o:",["benchmark=","catalogue=", "outputfile="])
    except getopt.GetoptError:
        print 'xml_stream_parser.py -b <benchmark> -c <catalogue> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'xml_stream_parser.py -b <benchmark> -c <catalogue> -o <outputfile>'
            sys.exit()
        elif opt in ("-b", "--benchmark"):
            benchmark = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-c", "--catalogue"):
            catalogue_file = arg
    if benchmark == '' or catalogue_file == '' or outputfile == '':
        print 'Usage: xml_stream_parser.py -b <benchmark> -c <catalogue> -o <outputfile>'
        sys.exit(2)

    print 'benchmark file is "', benchmark
    print 'Output file is "', outputfile

    w2v_path = 'all.norm-sz100-w10-cb0-it1-min100.w2v'

    w2v = gensim.models.KeyedVectors.load_word2vec_format(w2v_path, binary=True, unicode_errors='ignore')
    #new_hierarchy = build_ontology.build_new_hierarchy(benchmark, w2v)
    hierarchy = build_ontology.build_hierarchy(benchmark, w2v)
    catalogue_root = etree.parse(catalogue_file)
    catalogue = catalogue_root.getroot()
    categories = {}
    matched_cats = {}
    for coord in catalogue:
        for child in coord.getchildren():
            if child.tag == "categories":
                for cat in child:
                    category = {}
                    category["id"] = cat.get("id")
                    category["descr"] = cat.text
                    category["parentId"] = cat.get("parentId")
                    categories[category["id"]] = category
        i = 0
        for cat in categories.keys():
            #parents = getParents(categories, cat)
            #print parents
            #par_names = []
            #for par in parents:
            #    par_names.append(categories[par]["descr"])
            
            try:
                dummy = matched_cats[cat]
            except KeyError:
                hier_match = w2vconverter.match_cat(hierarchy, w2v, categories[cat]["descr"])
                matched_cats[cat] = hier_match[0]
                i = i + 1
                print i, "\t", categories[cat]["descr"], "\t", hier_match[0], "\t", hier_match[1]

        for child in coord.getchildren():
            if child.tag == "offers":
                for offer in child:
                    for field in offer:
                        if field.tag == "categoryId":
                            cat_name = categories[field.text]["descr"]
                            try:
                                match = matched_cats[field.text]
                                #print cat_name, ": ", match
                                newTag = etree.Element( "matchedCategory" )
                                newTag.text = match.decode("utf-8")
                                offer.append(newTag)
                            except KeyError:
                                next
    tree  = etree.ElementTree(catalogue)
    tree.write(outputfile, pretty_print=True, xml_declaration=True,   encoding="utf-8")

if __name__ == "__main__":
    main(sys.argv[1:])

