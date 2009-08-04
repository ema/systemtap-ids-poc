import sys
import seqtree

class SyscallDataReader(object):

    def __init__(self, input=sys.stdin):
        self.executables = {}
        
        while True:
            # Not using readlines() to allow unbuffered input
            try:
                sequence = input.readline()
            except KeyboardInterrupt:
                break

            if not sequence:
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
