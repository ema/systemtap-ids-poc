#!/usr/bin/python

import sys

import config
import reader
import dbaccess

from hamming import distance_xrange 

DATA = dbaccess.getdata()

def min_distance(sequence, known_seqs, distance=distance_xrange):
    minimum = config.SEQUENCE_LENGTHS

    for known in known_seqs:
        val = distance(known, sequence)
        if val <= config.ALLOWED_MISMATCHES:
            return val

        if val < minimum:
            minimum = val

    return minimum

def check_sequence(input_line):
    execname, uid, calls = reader.line2data(input_line)

    if execname not in DATA.executables:
        return None, None, None

    known_seqs = tuple(DATA.executables[execname])

    minimum = min_distance(calls, known_seqs)

    if minimum > config.ALLOWED_MISMATCHES:
        return minimum, execname, calls

    return None, None, None

def main():
    dbaccess.check_seq_length_consistency(DATA.sequence_lengths)

    while True:
        sequence = sys.stdin.readline()
        if not sequence:
            break

        minimum, execname, calls = check_sequence(sequence)

        if minimum:
            print minimum, execname, calls

if __name__ == "__main__":
    main()
