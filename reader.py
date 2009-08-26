import sys
import time

import seqtree

class SyscallDataReader(object):

    def __init__(self, input=sys.stdin, data_to_merge=None):
        if data_to_merge is not None:
            self.executables = data_to_merge
        else:
            self.executables = {}

        self.starting = time.time()
        
        while True:
            # Not using readlines() to allow unbuffered input
            try:
                sequence = input.readline()
            except KeyboardInterrupt:
                self.ending = time.time()
                break

            if not sequence:
                self.ending = time.time()
                break

            sequence = sequence.split()
            execname, calls = sequence[0], tuple(sequence[1:])

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
