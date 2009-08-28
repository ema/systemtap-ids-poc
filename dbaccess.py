import os
import shutil
import cPickle

import config

def dbexists():
    return os.path.isfile(config.FILENAME)

def getdata():
    dbf = open(config.FILENAME, 'r')
    reader = cPickle.loads(dbf.read())
    dbf.close()
    return reader

def putdata(data):
    if dbexists():
        backup = config.FILENAME + ".old"
        print "Creating backup file", backup, "before saving database...",
        shutil.copy(config.FILENAME, backup)
        print "done."

    # can't pickle file objects
    data.input = None

    dbf = open(config.FILENAME, 'wb')
    cPickle.dump(data, dbf)
    dbf.close()
