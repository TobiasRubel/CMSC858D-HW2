#!/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

def plot_binaries(out, figs):
    """
    plot the size of the binaries w.r.t reference size and prefix array size
    """

    # first collect all the data into a dataframe

    d = {}

    for a in os.listdir(out):
        percent_size, k, _ = a.split('-')
        percent_size = float(percent_size)
        k = int(k)
        mb = os.path.getsize(os.path.join(out,a))
        try:
            d[percent_size][k] = mb
        except:
            d[percent_size] = {}
            d[percent_size][k] = mb
    
    df = pd.DataFrame(d)
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.reindex(sorted(df.index), axis=0)
    fig, ax = plt.subplots(1, 2, figsize=(4, 3))
    df.mean(axis=0).plot(ax=ax[0])
    df.mean(axis=1).plot(ax=ax[1])
    ax[1].set_xlabel("preftable size")
    ax[0].set_xlabel("% of full ecoli reference")
    ax[0].set_ylabel("mean size (bytes)")
    ax[1].set_ylabel("mean size (bytes)")
    plt.tight_layout()
    plt.savefig(os.path.join(figs,"sizes.pdf"))

def plot_gen_time(timing, figs):
    """
    plot the time it took to make the suffix array and prefix tables
    """
    
    d_total = {}
    d_bsa = {}
    d_bpt = {}

    for t in [x for x in os.listdir(timing) if ".bt" in x]:
        percent_size, k, _ = t.split('-')
        percent_size = float(percent_size)
        k = int(k)
        with open(os.path.join(timing, t),'r') as f:
            bsa, bpt = [float(x) for x in f.readlines()]
            total = bsa + bpt
            try:
                d_total[percent_size][k] = total
                d_bsa[percent_size][k] = bsa
                d_bpt[percent_size][k] = bpt
            except:
                d_total[percent_size] = {}
                d_bsa[percent_size] = {}
                d_bpt[percent_size] = {}
                d_total[percent_size][k] = total
                d_bsa[percent_size][k] = bsa
                d_bpt[percent_size][k] = bpt

    df_total = pd.DataFrame(d_total)
    df_bsa = pd.DataFrame(d_bsa)
    df_bpt = pd.DataFrame(d_bpt)

    df_total = df_total.reindex(sorted(df_total.columns), axis=1)
    df_total = df_total.reindex(sorted(df_total.index), axis=0)

    df_bsa = df_bsa.reindex(sorted(df_bsa.columns), axis=1)
    df_bsa = df_bsa.reindex(sorted(df_bsa.index), axis=0)


    df_bpt = df_bpt.reindex(sorted(df_bpt.columns), axis=1)
    df_bpt = df_bpt.reindex(sorted(df_bpt.index), axis=0)

    print(df_total)
    fig, ax = plt.subplots(3, 2, figsize=(6, 5))
    df_total.mean(axis=0).plot(ax=ax[0][0])
    df_total.mean(axis=1).plot(ax=ax[0][1])
    
    df_bsa.mean(axis=0).plot(ax=ax[1][0])
    df_bsa.mean(axis=1).plot(ax=ax[1][1])

    df_bpt.mean(axis=0).plot(ax=ax[2][0])
    df_bpt.mean(axis=1).plot(ax=ax[2][1])

    for i in range(3):
        ax[i][0].set_xlabel("% of full ecoli reference")
        ax[i][1].set_xlabel("preftable size")
        ax[i][0].set_ylim((0,10))
        ax[i][1].set_ylim((0,10))
        ax[i][0].set_ylabel("time (s)")
        ax[i][1].set_ylabel("time (s)")

    ax[0][0].set_title("total time (SA + PT)")
    ax[0][1].set_title("total time (SA + PT)")

    ax[1][0].set_title("time for Suffix Array")
    ax[1][1].set_title("time for Suffix Array")


    ax[2][0].set_title("time for Prefix Table")
    ax[2][1].set_title("time for Prefix Table")



    plt.tight_layout()

    plt.savefig(os.path.join(figs,"creationtime.pdf"))


def plot_query_time(timing, figs):
    """
    plot the time it took to make the suffix array and prefix tables
    """
    
    d_naive = {}
    d_simpleaccel = {}

    d_naive_q = {}
    d_simpleaccel_q = {}

    for t in [x for x in os.listdir(timing) if ".qt" in x]:
        percent_size, k, qsize, mode, _ = t.split('-')
        percent_size = float(percent_size)
        k = int(k)
        qsize = int(qsize)
        with open(os.path.join(timing, t),'r') as f:
            t = float([x for x in f.readlines()][0])
            if mode == "naive":
                try:
                    d_naive[percent_size][k] += t
                except:
                    try:
                        d_naive[percent_size][k] = t
                    except:
                        d_naive[percent_size] = {}
                        d_naive[percent_size][k] = t
                try:
                    d_naive_q[percent_size][qsize] += t
                except:
                    try:
                        d_naive_q[percent_size][qsize] = t
                    except:
                        d_naive_q[percent_size] = {}
                        d_naive_q[percent_size][qsize] = t
            else:
                try:
                    d_simpleaccel[percent_size][k] += t
                except:
                    try:
                        d_simpleaccel[percent_size][k] = t
                    except:
                        d_simpleaccel[percent_size] = {}
                        d_simpleaccel[percent_size][k] = t
                        
                try:
                    d_simpleaccel_q[percent_size][qsize] += t
                except:
                    try:
                        d_simpleaccel_q[percent_size][qsize] = t
                    except:
                        d_simpleaccel_q[percent_size] = {}
                        d_simpleaccel_q[percent_size][qsize] = t       
    print(d_naive)
    print(d_naive_q)

    df_naive = pd.DataFrame(d_naive)
    df_simpleaccel = pd.DataFrame(d_simpleaccel)

    df_naive_q = pd.DataFrame(d_naive_q)
    df_simpleaccel_q = pd.DataFrame(d_simpleaccel_q)


    df_naive = df_naive.apply(lambda x: x / 60)
    df_simpleaccel = df_simpleaccel.apply(lambda x: x / 60)

    df_naive_q = df_naive_q.apply(lambda x: x / 60)
    df_simpleaccel_q = df_simpleaccel_q.apply(lambda x: x / 60)

    df_naive = df_naive.reindex(sorted(df_naive.columns), axis=1)
    df_naive = df_naive.reindex(sorted(df_naive.index), axis=0)

    df_simpleaccel = df_simpleaccel.reindex(sorted(df_simpleaccel.columns), axis=1)
    df_simpleaccel = df_simpleaccel.reindex(sorted(df_simpleaccel.index), axis=0)

    df_naive_q = df_naive_q.reindex(sorted(df_naive_q.columns), axis=1)
    df_naive_q = df_naive_q.reindex(sorted(df_naive_q.index), axis=0)

    df_simpleaccel_q = df_simpleaccel_q.reindex(sorted(df_simpleaccel_q.columns), axis=1)
    df_simpleaccel_q = df_simpleaccel_q.reindex(sorted(df_simpleaccel_q.index), axis=0)

    print(df_naive)
    print(df_naive_q)

    fig, ax = plt.subplots(2, 2, figsize=(5, 5))
    df_naive.plot(ax=ax[0][0])
    df_simpleaccel.plot(ax=ax[0][1])
    df_naive_q.plot(ax=ax[1][0])
    df_simpleaccel_q.plot(ax=ax[1][1])

    for i in range(2):
        ax[0][i].set_xlabel("preftable size")
        ax[1][i].set_xlabel("length of query")
        #ax[i][0].set_ylim((0,10))
        #ax[i][1].set_ylim((0,10))
        ax[i][0].set_ylabel("time (s)")
        ax[i][1].set_ylabel("time (s)")
        ax[i][0].set_title("naive")
        ax[i][1].set_title("simpleaccel")

    plt.tight_layout()

    plt.savefig(os.path.join(figs,"querytime.pdf"))
    #plt.show()


def main():
    """
    everything in this script is hardcoded
    """

    DATADIR="/home/tobias/Projects/CMSC858D/Project_2/data/report-data"
    TIMINGDIR=os.path.join(DATADIR,"timing")
    OUTDIR=os.path.join(DATADIR,"output")
    PLOTDIR=os.path.join(DATADIR,"figs")
    try:
        os.mkdir(PLOTDIR)
    except:
        pass

    # first let's plot the size of the binaries.
    plot_binaries(OUTDIR, PLOTDIR)

    # next the time it took to generate the files.
    plot_gen_time(TIMINGDIR, PLOTDIR)

    # next the time it took to perform queries.
    plot_query_time(TIMINGDIR, PLOTDIR)

if __name__ == "__main__":
    main()
