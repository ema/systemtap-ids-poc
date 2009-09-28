"""
Return the number of mismatches between two sequences

In [5]: seq1 = ('write', 'gettimeofday', 'ppoll', 'read', 'ioctl')
   ...: seq2 = ('write', 'gettimeofday', 'ppoll', 'read', 'write')

In [6]: distance(seq1, seq2)
Out[6]: 1
"""

import config

def distance_comprehension(s1, s2):
    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])

def distance_enumerate(seq1, seq2):
    mismatches = 0

    for idx, elem in enumerate(seq1):
        if elem != seq2[idx]:
            mismatches += 1

    return mismatches

def distance_xrange(seq1, seq2):
    mismatches = 0

    for idx in xrange(config.SEQUENCE_LENGTHS):
        if seq1[idx] != seq2[idx]:
            mismatches += 1

    return mismatches

if __name__ == "__main__":
    import timeit

    for what in "distance_comprehension", "distance_enumerate", "distance_xrange":
        print what,

        t = timeit.Timer("hamming.%s(('write', 'gettimeofday', 'ppoll', 'read', 'ioctl'), ('write', 'gettimeofday', 'ppoll', 'ppoll', 'ioctl'))" % what, "import hamming")

        vals = t.repeat(10, 100000)
        print min(vals), vals
