#!/bin/sh

stap syscall-sequence.stp | ./builddb.py 
