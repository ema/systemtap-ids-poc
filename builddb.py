#!/usr/bin/python

import sys
import cPickle

from reader import SetSyscallDataReader
import config

data = SetSyscallDataReader(input=sys.stdin)
executables = data.executables

dbf = open(config.FILENAME, 'wb')
cPickle.dump(data, dbf)
dbf.close()

print "Database built into", config.FILENAME

print "Unique syscalls sequences per executable name:"

for execname in executables:
    print execname, len(executables[execname])
