#!/usr/bin/env python
import re
import sys
# No use for multicore system
#from threading import Thread
from multiprocessing import Process

# Because my CPU has only 4 cores.
NUM_THREAD = 4

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
    global NUM_THREAD
    
    for i in xrange(NUM_THREAD):
        for j in xrange(NUM_THREAD):
            pr = Process(target = compute_jaccard_thread, args = (col1, col2, threshold, i, j))
            pr.start()

def compute_jaccard_thread(col1, col2, threshold, idx1, idx2):
    ''''Each thread compute a part, in modulo manner.'''
    global NUM_THREAD
    
    n1 = len(col1)
    n2 = len(col2)
    step = NUM_THREAD
    # If you write this part a different way, the performance is gonna suck.
    # Multicore programming is not easy.
    for i in xrange(idx1, n1, step):
        for j in xrange((idx1 + idx2) % step, n2, step):
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

