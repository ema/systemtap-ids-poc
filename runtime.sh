#!/bin/sh

nice -n 19 staprun -b 64 allsequences.ko | nice -n 19 python runtime_check.py
