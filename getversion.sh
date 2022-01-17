#!/usr/bin/env bash

grep "version =" ./src/homed.py | awk '{ print $3 }' | tr -d '"'
