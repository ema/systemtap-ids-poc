import timeit
import unittest

import StringIO

from reader import TreeSyscallDataReader, SetSyscallDataReader
import dbaccess

def _xcombinations(items, n):
    if n == 0: 
        yield []
    else:
        for i in xrange(len(items)):
            for cc in _xcombinations(items[:i]+items[i+1:],n-1):
                yield [items[i]]+cc

def _testfd():
    syscalls = [
        'futex', 'gettimeofday', 'write',
        'recvfrom', 'recv', 'rt_sigprocmask', 'time' 'stat'
    ]

    sequences = [ w for w in _xcombinations(syscalls, 5) ]

    testfd = StringIO.StringIO()
    for execname in 'firefox', 'syslogd':
        for seq in sequences:
            testfd.write("%s %s\n" % (execname, " ".join(seq)))

    testfd.seek(0)
    return testfd

class TestReader(unittest.TestCase):
    classname = None

    known_seq = {
        #'firefox': ('futex', 'gettimeofday', 'futex', 'write', 'gettimeofday' ),
        'syslogd': ('timestat', 'rt_sigprocmask', 'recvfrom', 'futex', 'write'),
    }

    def setUp(self):
        self.reader = self.classname(_testfd())

    def testKnownSeq(self):
        for execname, seq in self.known_seq.items():
            self.assertTrue(self.reader.knownseq(execname, seq))

    def testAddSeq(self):
        execname = 'mutt'
        sequence = ('futex', 'gettimeofday', 'write', 'time' 'stat')
        self.reader.addseq(execname, sequence)

    def testActualData(self):
        try:
            self.reader = self.classname(open("/var/tmp/rawdata.allsequences"))
        except IOError:
            print "\nNo raw data available. Skipping testActualData."
            return

        def known1():
            sequence = ( "gettimeofday", "read", "gettimeofday", 
                         "gettimeofday", "gettimeofday" )
            self.assertTrue(self.reader.knownseq("firefox", sequence))

        def known2():
            sequence = ("read", "ioctl", "ioctl", "ioctl", "ioctl")
            self.assertTrue(self.reader.knownseq("pulseaudio", sequence))

        def unknown():
            sequence = ("read", "ioctl", "b", "c", "d")
            self.assertFalse(self.reader.knownseq("pulseaudio", sequence))

        t = timeit.Timer(known1)
        print t.timeit()

        t = timeit.Timer(known2)
        print t.timeit()

        t = timeit.Timer(unknown)
        print t.timeit()

class TestTreeSyscallDataReader(TestReader):
    classname = TreeSyscallDataReader

class TestSetSyscallDataReader(TestReader):
    classname = SetSyscallDataReader

class TestDbAccess(unittest.TestCase):

    def test_01_getdata(self):
        data = dbaccess.getdata()
        self.failUnless(len(data.executables.keys()) > 0)

        for sequences in data.executables.values():
            for seq in sequences:
                self.assertEquals(len(seq), 5)

    def test_02_putdata(self):
        # fail if fake executable is present BEFORE putdata
        data = dbaccess.getdata()
        self.failIf("no such executable" in data.executables)

        # adding fake executable 
        data.executables["no such executable"] = [ 
            ('no', 'such', 'sequence'), 
        ]
        dbaccess.putdata(data)

        # fail if NOT present AFTER putdata
        data = dbaccess.getdata()
        self.failUnless("no such executable" in data.executables)
        
        # removing
        del data.executables["no such executable"]
        dbaccess.putdata(data)

        # fail if fake executable is present after removing it
        data = dbaccess.getdata()
        self.failIf("no such executable" in data.executables)
        
if __name__ == "__main__":
    to_run = (TestSetSyscallDataReader, 
              TestTreeSyscallDataReader, 
              TestDbAccess)

    for what in to_run:
        suite = unittest.TestLoader().loadTestsFromTestCase(what)
        unittest.TextTestRunner(verbosity=2).run(suite)
