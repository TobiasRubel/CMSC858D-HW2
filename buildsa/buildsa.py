#!/bin/python3

import numpy as np
import sys
from Bio import SeqIO
from pydivsufsort import divsufsort, kasai
import pickle
from itertools import product
import time
import warnings
warnings.filterwarnings("ignore")


def read_fasta(fasta):
    """
    :f       /path/to/fasta-file
    :returns string sequence
    """
    with open(fasta, 'r') as f:
        S = SeqIO.parse(f, 'fasta')
        return str(next(S).seq+"$")

def _find_interval(c,SA,ref,k):
    start = -1
    end = -1
    for i in range(len(SA)):
        if ref[SA[i]:SA[i]+k] == c:
            start = i
        else:
            if start != -1:
                end = i
                return (start, end)

    return (start, end)


def _construct_preftab(ref,SA,k):
    """
    :need to find the first and last element of the suffix array with prefix p for all k-length p
    """
    dictionary = "ACTG"
    combos = np.array(["".join(x) for x in product(dictionary, repeat=k)])
    print(combos)
    preftab = {}
    for c in combos:
        preftab[c] = _find_interval(c, SA, ref, k)
    return preftab


def construct_preftab(S, SA, k):
    start = -1
    pref = ''
    tab = {}
    for i in range(len(SA)):
        curr_pref = S[SA[i]:SA[i]+k]
        if curr_pref != pref:
            tab[pref] = (start, i)
            pref = curr_pref
            start = i
    del tab['']
    return tab


def construct_sa(ref, t = True):
    """
    :preftab int
    :ref     path/to/reference
    :returns suffix array over reference, LCP array over SA
    """
    S =  read_fasta(ref)
    if t:
        start = time.time()
    SA = divsufsort(S)
    if t:
        end = time.time()
        took = end - start
        print(took)

    return SA, S




def main(argv):
    DEBUG = False
    t = True
    k = 0
    ref = ''
    output = ''
    pdf = ''
    preftab = {}

    if argv[1] == "--prefix":
        k = int(argv[2])
        ref = argv[3]
        output = argv[4]
    else:
        ref = argv[1]
        output = argv[2]

    if DEBUG == True:
        print("preftab: {}\nref: {}\noutput: {}\n".format(k,ref,output))

    SA, S = construct_sa(ref)
    if t:
        start = time.time()
    if k != 0:
        preftab = construct_preftab(S, SA, k)
    if t:
        end = time.time()
        took = end - start
        print(took)

    # now let's save it
    with open(output,'wb') as f:
        pickle.dump((SA, S, preftab, k), f)
    


if __name__ == "__main__":
    main(sys.argv)
