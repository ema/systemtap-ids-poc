#!/bin/bash

. config.py

stap -DSTP_NO_OVERLOAD -s 64 -vvv -p 4 all-sequences.stp -m allsequences.ko $SEQUENCE_LENGTHS
