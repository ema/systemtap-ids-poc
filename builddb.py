#!/usr/bin/python

FILENAME = "/tmp/ids.db"

import sys
import cPickle

from reader import SetSyscallDataReader

data = SetSyscallDataReader(input=sys.stdin)
executables = data.executables

dbf = open(FILENAME, 'wb')
cPickle.dump(data, dbf)
dbf.close()

print "Database built into", FILENAME

print "Unique syscalls sequences per executable name:"

for execname in executables:
    print execname, len(executables[execname])
