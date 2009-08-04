#!/usr/bin/python 

def addseq(tree, sequence):
    """Add the given sequence to tree"""
    if sequence:
        elem = sequence[0]

        if elem not in tree:
            tree[elem] = {}

        addseq(tree[elem], sequence[1:])

def _seqintree(tree, sequence):
    try:
        elem = sequence[0]
    except IndexError:
        return True

    if elem not in tree:
        return False

    return _seqintree(tree[elem], sequence[1:])

def seqintree(tree, sequence):
    """Check if the given sequence is in tree"""
    return sequence and _seqintree(tree, sequence)

if __name__ == "__main__":
    # usage examples
    syscalls = [
        'open', 'mmap', 'read', 'write', 
        'close', 'seek', 'brk', 'select'
    ]

    def xcombinations(items, n):
        if n == 0: 
            yield []
        else:
            for i in xrange(len(items)):
                for cc in xcombinations(items[:i]+items[i+1:],n-1):
                    yield [items[i]]+cc
    #

    sequences = [ w for w in xcombinations(syscalls, 4) ] * 1000

    tree = {}

    print "Building tree of %s sequences:" % len(sequences)

    import time
    start = time.time()

    for seque in sequences:
        addseq(tree, seque)
        assert seqintree(tree, seque)

    print time.time() - start, "secs"

    assert seqintree(tree, [ 'open', 'mmap', 'read', 'write' ])

    assert not seqintree(tree, [ 'read', 'mmap', 'mmap', 'read' ])

    import pprint
    pprint.pprint(tree)
