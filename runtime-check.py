#!/usr/bin/python

FILENAME = "/tmp/ids.db"

import sys
import cPickle

dbf = open(FILENAME, 'r')
reader = cPickle.loads(dbf.read())
dbf.close()

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
