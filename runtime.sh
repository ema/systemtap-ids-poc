#!/bin/sh

nice -n 19 staprun allsequences.ko | nice -n 19 python -u runtime-check.py
