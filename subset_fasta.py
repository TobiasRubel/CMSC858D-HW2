#!/bin/python3

import os
import sys

def main(argv):
    i = argv[1]
    o = argv[2]
    p = float(argv[3])
    otname = "{}-".format(p)+os.path.basename(i)
    with open(i, 'r') as f:
        with open(os.path.join(o, otname), 'w') as g:
            for line in f.readlines():
                if line[0] == ">":
                    g.write(line)
                else:
                    num_chars = int(len(line)*p)
                    g.write(line[:num_chars])
    return 0
                    


if __name__ == "__main__":
    main(sys.argv)

