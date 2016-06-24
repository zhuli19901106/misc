#!/usr/bin/env python

from __future__ import print_function
import sys
from pyspark import SparkContext

threshold = 0

def jaccard_similarity(s1, s2):
    ni = len(s1 & s2)
    nu = len(s1 | s2)
    return 1.0 * ni / nu if nu > 0 else 1.0

def mapper(pair):
    global threshold
    
    s1 = set(pair[0][0].split())
    s2 = set(pair[1][0].split())
    id1 = pair[0][1]
    id2 = pair[1][1]
    similarity = jaccard_similarity(s1, s2)
    return (id1, id2, similarity)
    
def get_dataset_rdd(sc, file_name):
    return sc.textFile(file_name)\
             .map(lambda s: s.strip())\
             .filter(lambda s: len(s) > 0)\
             .zipWithIndex()
    
def main():
    global threshold
    
    if len(sys.argv) < 4:
        print('Usage: jaccard-similarity.py <input1> <input2> <threshold>')
        exit(1)
    
    sc = SparkContext("local", "JaccardSimilarity");
    
    file_name1 = sys.argv[1]
    file_name2 = sys.argv[2]
    threshold = float(sys.argv[3])
    
    rdd1 = get_dataset_rdd(sc, file_name1)
    rdd2 = get_dataset_rdd(sc, file_name2)
    pair_rdd = rdd1.cartesian(rdd2)
    
    result = pair_rdd.map(mapper)\
                     .filter(lambda tp: tp[2] > threshold)\
                     .map(lambda tp: '%d\t%d\t%f' % (tp[0], tp[1], tp[2]))\
                     .collect()
    for single_result in result:
        print(single_result)
    
if __name__ == '__main__':
    main()
    
