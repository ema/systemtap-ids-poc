import timeit
import unittest

import StringIO

from reader import TreeSyscallDataReader, SetSyscallDataReader
import config
import dbaccess
import hamming
import runtime_check

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

    sequences = [ w for w in _xcombinations(syscalls, config.SEQUENCE_LENGTHS) ]

    testfd = StringIO.StringIO()
    for execname in 'firefox', 'syslogd':
        for seq in sequences:
            testfd.write("%s 1000 %s\n" % (execname, " ".join(seq)))

    testfd.seek(0)
    return testfd

def _gen_sequence_from_seed(seed):
    # seed is a tuple of syscalls
    # eg: ('futex', 'gettimeofday', 'write', 'time' 'stat' )
    return tuple([ seed[iteration % len(seed) ] 
        for iteration in range(config.SEQUENCE_LENGTHS) ])

class TestReader(unittest.TestCase):
    classname = None

    def setUp(self):
        self.reader = self.classname(_testfd())
        self.known_seq = {}

        for executable in 'firefox', 'syslogd':
            self.known_seq[executable] = tuple(self.reader.executables[executable])[0]

    def testKnownSeq(self):
        for execname, seq in self.known_seq.items():
            self.assertTrue(self.reader.knownseq(execname, seq))

    def testAddSeq(self):
        execname = 'mutt'
        sequence = _gen_sequence_from_seed(
            ('futex', 'gettimeofday', 'write', 'time' 'stat' ))
        
        self.reader.addseq(execname, sequence)

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
                self.assertEquals(len(seq), config.SEQUENCE_LENGTHS)

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

class TestRuntime(unittest.TestCase):
    
    def __min_distance_best_case(self, known_seqs):
        sequence = known_seqs[0]
        self.assertEquals(0, runtime_check.min_distance(sequence, known_seqs))

    def __min_distance_worst_case(self, known_seqs):
        sequence = _gen_sequence_from_seed(( 'wrong', ))
        self.assertEquals(len(sequence), runtime_check.min_distance(sequence, known_seqs))

    def test_01_min_distance_fake_data(self):
        known_seqs = [
            _gen_sequence_from_seed(('futex', 'gettimeofday', 'rite', 'time' 'stat' )),
            _gen_sequence_from_seed(('futex', 'gettimeofday', 'write', 'time' 'stat' )),
        ]

        self.__min_distance_best_case(known_seqs)

        sequence = _gen_sequence_from_seed(( 'futex', 'gettimeofday', ))
        self.assertEquals(2, runtime_check.min_distance(sequence, known_seqs))

        sequence = _gen_sequence_from_seed(( 'gettimeofday', ))
        self.assertEquals(4, runtime_check.min_distance(sequence, known_seqs))

        self.__min_distance_worst_case(known_seqs)

    def test_02_min_distance_real_data(self):
        data = dbaccess.getdata()
        known_seqs = tuple(data.executables[data.executables.keys()[0]])

        self.__min_distance_best_case(known_seqs)
        self.__min_distance_worst_case(known_seqs)

    def test_03_min_distance_benchmark(self):
        setup = """
import runtime_check
from hamming import distance_comprehension, distance_enumerate, distance_xrange
import dbaccess
from tests import _gen_sequence_from_seed

data = dbaccess.getdata()
known_seqs = tuple(data.executables[data.executables.keys()[0]])
sequence = _gen_sequence_from_seed(( 'wrong', ))
"""
        statement = "runtime_check.min_distance(sequence, known_seqs, %s)"

        values = []

        for func in ("distance_comprehension", "distance_enumerate", "distance_xrange"):
            t = timeit.Timer(statement % func, setup)
            values.append(min(t.repeat(3, 100)))
            
        print values
        self.failUnless(values[0] > values[1] > values[2])

if __name__ == "__main__":
    to_run = (
        TestSetSyscallDataReader, 
        TestTreeSyscallDataReader, 
        TestDbAccess,
        TestRuntime,
    )

    for what in to_run:
        suite = unittest.TestLoader().loadTestsFromTestCase(what)
        unittest.TextTestRunner(verbosity=2).run(suite)
