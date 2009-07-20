#!/usr/bin/python

FILENAME = "/tmp/ids.db"

import sys
import cPickle

executables = {}

for sequence in sys.stdin.readlines():
    sequence = sequence.split()

    execname, calls = sequence[0], tuple(sequence[1:])
    
    if execname not in executables:
        executables[execname] = set([calls])
    else:
        executables[execname].add(calls)

dbf = open(FILENAME, 'wb')
cPickle.dump(executables, dbf)
dbf.close()

print "Database built into", FILENAME

print "Unique syscalls sequences per executable name:"

for execname in executables:
    print execname, len(executables[execname])
