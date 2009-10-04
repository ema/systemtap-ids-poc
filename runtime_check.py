#!/usr/bin/python

import sys

import config
import reader
import dbaccess

from hamming import distance_xrange 

def min_distance(sequence, known_seqs, distance=distance_xrange):
    minimum = config.SEQUENCE_LENGTHS

    for known in known_seqs:
        val = distance(known, sequence)
        if val <= config.ALLOWED_MISMATCHES:
            return val

        if val < minimum:
            minimum = val

    return minimum

def main():
    data = dbaccess.getdata()
    dbaccess.check_seq_length_consistency(data.sequence_lengths)

    while True:
        input_line = sys.stdin.readline()
        if not input_line:
            break

        execname, uid, calls = reader.line2data(input_line)

        if execname not in data.executables:
            continue

        known_seqs = tuple(data.executables[execname])

        minimum = min_distance(calls, known_seqs)

        if minimum > config.ALLOWED_MISMATCHES:
            print minimum, execname, calls

if __name__ == "__main__":
    main()
