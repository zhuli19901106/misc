#!/usr/bin/env python
import sys

DELIMITER = '#'

def read_dataset(file_name):
    f = open(file_name, 'r')
    dataset = f.readlines()
    f.close()
    return map(lambda x: x.strip(), dataset)

def cartesian_product(file_name1, file_name2):
    '''Compute Jaccard similarity for two collecton.'''
    global DELIMITER
    
    f = open(file_name1, 'r')
    col1 = map(lambda x: x.strip(), f.readlines())
    f.close()
    
    f = open(file_name2, 'r')
    col2 = map(lambda x: x.strip(), f.readlines())
    f.close()
    
    n1 = len(col1)
    n2 = len(col2)
    for i in xrange(n1):
        for j in xrange(n2):
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
    
