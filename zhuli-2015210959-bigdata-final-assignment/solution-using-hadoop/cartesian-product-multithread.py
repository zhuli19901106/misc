#!/usr/bin/env python
import sys
from multiprocessing import Process

NUM_THREAD = 4
DELIMITER = '#'

def read_dataset(file_name):
    f = open(file_name, 'r')
    dataset = f.readlines()
    f.close()
    return map(lambda x: x.strip(), dataset)

def cartesian_product(file_name1, file_name2):
    '''Compute Jaccard similarity for two collecton.'''
    global NUM_THREAD
    
    f = open(file_name1, 'r')
    col1 = map(lambda x: x.strip(), f.readlines())
    f.close()
    
    f = open(file_name2, 'r')
    col2 = map(lambda x: x.strip(), f.readlines())
    f.close()
        
    for i in xrange(NUM_THREAD):
        for j in xrange(NUM_THREAD):
            pr = Process(target = cartesian_product_thread, args = (col1, col2, i, j))
            pr.start()

def cartesian_product_thread(col1, col2, idx1, idx2):
    ''''Each thread compute a part, in modulo manner.'''
    global NUM_THREAD, DELIMITER
    
    n1 = len(col1)
    n2 = len(col2)
    step = NUM_THREAD
    # If you write this part a different way, the performance is gonna suck.
    # Multicore programming is not easy.
    for i in xrange(idx1, n1, step):
        for j in xrange((idx1 + idx2) % step, n2, step):
            print(col1[i] + DELIMITER + col2[j])
            
def main():
    global NUM_THREAD
    
    if len(sys.argv) < 3:
        print('Usage cartesian-product <input1> <input2>')
        sys.exit(1)
    file_name1 = sys.argv[1]
    file_name2 = sys.argv[2]
    cartesian_product(file_name1, file_name2)
    
if __name__ == '__main__':
    main()
    
