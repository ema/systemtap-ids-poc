import sys
import time

import config
import seqtree

def line2data(input_line):
    input_line = input_line.split()
    # eg: Xorg 0 select clock_gettime setitimer read mmap2
    (execname, uid), calls = input_line[:2], tuple(input_line[2:])
    return execname, uid, calls

class SyscallDataReader(object):

    def __init__(self, input=sys.stdin, data_to_merge=None):
        if data_to_merge is not None:
            self.executables = data_to_merge
        else:
            self.executables = {}

        self.starting = time.time()
        self.input = input

        self.sequence_lengths = config.SEQUENCE_LENGTHS
        
        try:
            self.go()
        except KeyboardInterrupt:
            print "Done"
        
        self.ending = time.time()

    def go(self):
        while True:
            # Not using readlines() to allow unbuffered input
            input_line = self.input.readline()

            if not input_line:
                self.ending = time.time()
                break

            execname, uid, calls = line2data(input_line)
            self.addseq(execname, calls)

    def addseq(self, execname, calls):
        raise NotImplementedError

    def knownseq(self, execname, calls):
        raise NotImplementedError

class TreeSyscallDataReader(SyscallDataReader):

    def addseq(self, execname, calls):
        if execname not in self.executables:
            self.executables[execname] = {}

        seqtree.addseq(self.executables[execname], calls)       

    def knownseq(self, execname, calls):
        return seqtree.seqintree(self.executables[execname], calls)

class SetSyscallDataReader(SyscallDataReader):

    def addseq(self, execname, calls):
        if execname not in self.executables:
            self.executables[execname] = set([])

        self.executables[execname].add(calls)

    def knownseq(self, execname, calls):
        return calls in self.executables[execname]
