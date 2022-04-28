#!/bin/python3


import sys
import os
import random


def gen_query(s):
    """
    :returns query of size s 
    """
    dictionary = ["A", "C", "T", "G"]
    return "".join(random.choices(dictionary,k=s))+"\n"

def main(argv):
    o = argv[1]
    s = int(argv[2])
    n = 10
    
    nm = "{}-queries.fa".format(s)
    with open(os.path.join(o,nm),'w') as f:
        for i in range(n):
            f.write(">{}\n".format(i))
            f.write(gen_query(s))


if __name__ == "__main__":
    main(sys.argv)
