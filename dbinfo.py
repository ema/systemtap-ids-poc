#!/usr/bin/python

FILENAME = "/tmp/ids.db"

import os
import cPickle

print "Database size:", os.stat(FILENAME).st_size / 1024, "KB\n"

dbf = open(FILENAME, 'r')
reader = cPickle.loads(dbf.read())
dbf.close()

execnames = reader.executables.keys()
print len(execnames), "executables\n"

with_counts = [ (len(reader.executables[execname]), execname)
    for execname in execnames ]

print "Top 10:"

for data in sorted(with_counts, reverse=True)[:10]:
    print data[1], data[0]

print
print round((reader.ending - reader.starting) / 60), "minutes"
