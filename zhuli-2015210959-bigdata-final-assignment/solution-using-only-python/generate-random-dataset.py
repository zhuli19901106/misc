#!/usr/bin/env python
import sys
from random import seed,randint

N = 26
MAX_ID = 1 << N
MASK = []

def id_to_list(id):
    global N, MASK
    v = []
    for i in xrange(N):
        if not (id & MASK[i]):
            continue
        v.append(chr(ord('a') + i))
    return v

def generate_single_record(id):
    global MAX_ID
    id = randint(0, MAX_ID)
    st = id_to_list(id)
    return st

def generate_dataset(num_dataset):
    seed()
    for i in xrange(num_dataset):
        print(' '.join(generate_single_record(id)))

def main():
    global MASK
    
    if len(sys.argv) < 2:
        print('Usage generate-random-dataset <number-of-datasets>')
        sys.exit(1)
    num_dataset = int(sys.argv[1])
    
    for i in xrange(26):
        MASK.append(1 << i)
    generate_dataset(num_dataset)

if __name__ == '__main__':
    main()

