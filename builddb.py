#!/usr/bin/python

import os
import sys

from reader import SetSyscallDataReader
import config
import dbaccess

msg = "%s database. Stop at any time with CTRL+C"

if not os.path.isfile(config.FILENAME):
    print msg % "Creating"
    data = SetSyscallDataReader(input=sys.stdin)

else:
    print "Loading old data...",
    reader = dbaccess.getdata()
    print "done"

    print msg % "Updating"

    data = SetSyscallDataReader(input=sys.stdin, 
        data_to_merge=reader.executables)

dbaccess.putdata(data)

print "Database built into", config.FILENAME

print "Unique syscalls sequences per executable name:"

for execname in data.executables:
    print execname, len(data.executables[execname])
