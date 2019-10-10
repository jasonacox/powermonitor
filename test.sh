#!/bin/bash
export PLUGID=$0 
export PLUGIP=$1
export PLUGKEY=$2
export PLUGVERS=${3:-'3.1'}

echo "JSON Output - plugjson.py:"
./plugjson.py
echo
echo "TEXT Output - plugpower.py:"
./plugpower.py