#!/usr/bin/env python
import sys

DELIMITER = '#'

def main():
    global DELIMITER
    
    if len(sys.argv) < 2:
        print('Usage add-line-number <input>')
        sys.exit(1)
    file_name = sys.argv[1]
    f = open(file_name, 'r')
    lines = f.readlines()
    line_number = 0
    for line in lines:
        print('%d#%s' % (line_number, line.strip()))
        line_number += 1

if __name__ == '__main__':
    main()

