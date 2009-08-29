#!/bin/sh

[ -f "allsequences.ko" ] || make build

nice -n 19 staprun -b 64 allsequences.ko | nice -n 19 python builddb.py 
