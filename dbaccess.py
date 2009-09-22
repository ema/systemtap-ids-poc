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

def check_seq_length_consistency(curlength):
    MSG = """
==============================================================================
Your old database has been created with a sequence length=%s, but your current 
configuration uses sequence length=%s.
Please remove %s and allsequences.ko, then run createdb.sh again.

Otherwise, if you're OK with sequence of length %s, just change the relevant 
setting in config.py
==============================================================================
""" % (curlength, config.SEQUENCE_LENGTHS, config.FILENAME, curlength)

    assert curlength == config.SEQUENCE_LENGTHS, MSG
