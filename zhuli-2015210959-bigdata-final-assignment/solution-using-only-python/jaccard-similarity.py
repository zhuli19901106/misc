#!/usr/bin/env python
import re
import sys

def jaccard_index(s1, s2):
    '''Compute the Jaccard index for two sets.'''
    if len(s1) == 0 and len(s2) == 0:
        return 1.0
    return 1.0 * len(s1 & s2) / len(s1 | s2)

def process_input(file_name):
    '''Process input documents, convert them into collections of sets.'''
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    res = map(set, map(lambda x: x.strip().split(), lines))
    
    return res

def compute_jaccard(col1, col2, threshold):
    '''Compute Jaccard similarity for two collecton.'''
    n1 = len(col1)
    n2 = len(col2)
    for i in xrange(n1):
        for j in xrange(n2):
            ji = jaccard_index(col1[i], col2[j])
            if ji <= threshold:
                continue
            print('%d %d %.3f' % (i, j, ji))

def main():
    if len(sys.argv) < 4:
        print('Usage: jaccard-similarity.py <input1> <input2> <threshold>')
        exit(1)
    input1 = sys.argv[1]
    input2 = sys.argv[2]
    threshold = float(sys.argv[3])
    
    col1 = process_input(input1)
    col2 = process_input(input2)

    compute_jaccard(col1, col2, threshold)

if __name__ == '__main__':
    main()

