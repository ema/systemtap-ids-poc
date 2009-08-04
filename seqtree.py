#!/usr/bin/python 

"""Tree-like data structure based on a dictionary of dictionaries.

Useful to store unique sequences of elements"""

def addseq(tree, sequence):
    """Add the given sequence to tree"""
    if sequence:
        elem = sequence[0]

        if elem not in tree:
            tree[elem] = {}

        addseq(tree[elem], sequence[1:])

def seqintree(tree, sequence):
    """Check if the given sequence is in tree"""
    try:
        elem = sequence[0]
    except IndexError:
        return True

    if elem not in tree:
        return False

    return seqintree(tree[elem], sequence[1:])
