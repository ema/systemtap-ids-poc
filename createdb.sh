#!/bin/sh

[ -f "allsequences.ko" ] || ./build-kernel-module.sh

nice -n 19 staprun -b 64 allsequences.ko | nice -n 19 python builddb.py 
