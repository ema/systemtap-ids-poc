import cPickle

import config

def getdata():
    dbf = open(config.FILENAME, 'r')
    reader = cPickle.loads(dbf.read())
    dbf.close()
    return reader

def putdata(data):
    dbf = open(config.FILENAME, 'wb')
    cPickle.dump(data, dbf)
    dbf.close()
