#!/bin/bash

PREFSIZES=( 0 2 4 8 10 12 )
REFSIZES=( 0.1 0.3 0.5 0.7 0.9 1.0 )
QRYSIZES=( 10 20 30 40 50 60 60 80 90 100 )
MODES=( 'naive' 'simpleaccel')

REFPATH=/home/tobias/Projects/CMSC858D/Project_2/data/CMSC858D_S22_Project2_sample/ecoli.fa
QRYPATH=/home/tobias/Projects/CMSC858D/Project_2/data/CMSC858D_S22_Project2_sample/query.fa
DATADIR=/home/tobias/Projects/CMSC858D/Project_2/data/report-data
TIMINGDIR=$DATADIR/timing
OUTDIR=$DATADIR/output

#initialize directory with data and stuff

if [ ! -e $DATADIR ]; then
    mkdir $DATADIR;
    mkdir $TIMINGDIR;
    mkdir $OUTDIR;

    for REF in ${REFSIZES[@]}; do
        python3 subset_fasta.py $REFPATH $DATADIR $REF;
    done

    for QRY in ${QRYSIZES[@]}; do
        python3 generate_sequences.py $DATADIR $QRY;
    done


fi
#do computations

for PREF in ${PREFSIZES[@]}; do
    for REF in ${REFSIZES[@]}; do
        # generate suffix array
        if [ $PREF -eq 0 ]; then
            python3 buildsa.py $DATADIR/$REF-ecoli.fa $OUTDIR/$REF-$PREF-ecoli.pkl > $TIMINGDIR/$REF-$PREF-ecoli.bt
        else

            python3 buildsa.py --prefix $PREF $DATADIR/$REF-ecoli.fa $OUTDIR/$REF-$PREF-ecoli.pkl > $TIMINGDIR/$REF-$PREF-ecoli.bt
        fi
        for MODE in ${MODES[@]}; do
            for QRY in ${QRYSIZES[@]}; do
                python3 querysa.py $OUTDIR/$REF-$PREF-ecoli.pkl $DATADIR/$QRY-queries.fa $MODE time > $TIMINGDIR/$REF-$PREF-$QRY-$MODE-ecoli.qt &
            done
            wait
        done
    done
done


