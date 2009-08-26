#!/usr/bin/python

import os
import sys
import cPickle

from reader import SetSyscallDataReader
import config

msg = "%s database. Stop at any time with CTRL+C"

if not os.path.isfile(config.FILENAME):
    print msg % "Creating"
    data = SetSyscallDataReader(input=sys.stdin)

else:
    print "Loading old data...",
    dbf = open(config.FILENAME, 'r')
    reader = cPickle.loads(dbf.read())
    dbf.close()
    print "done"

    print msg % "Updating"

    data = SetSyscallDataReader(input=sys.stdin, 
        data_to_merge=reader.executables)

executables = data.executables

dbf = open(config.FILENAME, 'wb')
cPickle.dump(data, dbf)
dbf.close()

print "Database built into", config.FILENAME

print "Unique syscalls sequences per executable name:"

for execname in executables:
    print execname, len(executables[execname])
