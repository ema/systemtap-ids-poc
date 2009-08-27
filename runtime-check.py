#!/usr/bin/python

import sys
import cPickle

import config
import dbaccess

def distance(seq1, seq2):
    """
    Return the number of mismatches between two sequences

    In [5]: seq1 = ('write', 'gettimeofday', 'ppoll', 'read', 'ioctl')
       ...: seq2 = ('write', 'gettimeofday', 'ppoll', 'read', 'write')

    In [6]: runtime_check.distance(seq1, seq2)
    Out[6]: 1
    """
    mismatches = 0

    for idx, elem in enumerate(seq1):
        if elem != seq2[idx]:
            mismatches += 1

    return mismatches

if __name__ == "__main__":
    reader = dbaccess.getdata()

    while True:
        sequence = sys.stdin.readline()
        if not sequence:
            break

        sequence = sequence.split()

        execname, calls = sequence[0], tuple(sequence[1:])

        if execname not in reader.executables:
            continue

        if not reader.knownseq(execname, calls):
            print execname, calls
