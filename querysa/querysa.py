#!/bin/python3

import numpy as np
import sys
from Bio import SeqIO
from pydivsufsort import divsufsort, kasai
import pickle
import math
import time


def naive_query(S, SA, preftab, k, P, m):
    if k == 0:
        l = 0
        r = len(SA)
    else:
        try:
            l, r = preftab[P[:k]]
        except:
            #if except then the prefix of the query isn't in the ref
            return 0
        
    while l < r:
        c = math.floor((r+l)/2)
        SA_c = S[SA[c]:]

        if P < SA_c:
            if c == l + 1:
                return c
            else:
                r = c

        elif P > SA_c:
            if c == r - 1:
                return r
            else:
                l = c
    return 0



def LCP(a, b):
    i = 0
    while i < min(len(a), len(b)):
        if a[i] != b[i]:
            break
        i += 1
    return i

    
def simpleaccel_query(S, SA, preftab, k, P, m):
    
    if k == 0:
        l = 0
        r = len(SA)
    else:
        try:
            l, r = preftab[P[:k]]
        except:
            #if except then the prefix of the query isn't in the ref
            return 0
    
    c = math.floor((r+l)/2)

    l_lcp = LCP(P, S[SA[l]:])
    try:
        r_lcp = LCP(P, S[SA[r]:])
    except:
        r_lcp = 0
    c_lcp = min([l_lcp, r_lcp])
        
    while l < c:
        c = math.floor((r+l)/2)
        m_lcp = LCP(P, S[SA[c]:])
        c_lcp = min([l_lcp, r_lcp])
        SA_c = S[SA[c]:]

        if P[c_lcp:] < SA_c[c_lcp:]:
            if c == l + 1:
                return c
            else:
                r = c
                l_lcp = m_lcp

        elif P[c_lcp:] > SA_c[c_lcp:]:
            if c == r - 1:
                return r
            else:
                l = c
                r_lcp = m_lcp
    return 0

def query_sa(S, SA, preftab, k, queries, mode):
    m = len(S)
    if mode == "naive":
        _query = naive_query
    else:
        _query = simpleaccel_query

    with open(queries, 'r') as f:
        seqs = SeqIO.parse(f, 'fasta')
        for s in seqs:
            q = str(s.seq)
            query_name = str(s.id)
            lb = _query(S, SA, preftab, k, q+"#", m)
            ub = _query(S, SA, preftab, k, q+"{", m) 
            yield query_name, ub - lb, [str(SA[i]) for i in range(lb,ub)]


def main(argv):
    DEBUG = False
    index = ''
    queries = ''
    query_mode = ''
    output = ''

    index = argv[1]
    queries = argv[2]
    query_mode = argv[3]
    assert (query_mode == "naive") or (query_mode == "simpleaccel")
    output = argv[4]

    # load the index
    with open(index, 'rb') as f:
        (SA, S, preftab, k) = pickle.load(f)
    
    # compute things, write to file
    if output != 'time':
        with open(output, 'w') as f:
            for nm, cnt, vals in query_sa(S, SA, preftab, k, queries, query_mode):
                f.write("{}\t{}\t{}\n".format(nm, cnt, " ".join(vals)))
    else:
        start = time.time()
        for nm, cnt, vals in query_sa(S, SA, preftab, k, queries, query_mode):
            pass
        end = time.time()
        took = end - start
        print(took)
            

if __name__ == "__main__":
    main(sys.argv)
