#!/bin/sh

JOBS=250

rm -f *.spthy

parallel --jobs $JOBS < generate_command

