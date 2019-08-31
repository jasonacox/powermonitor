#!/bin/bash
export PLUGID='01234567891234567890' 
export PLUGIP="10.1.1.1" 
export PLUGKEY="0123456789abcdef"
echo "JSON Output - plugjson.py:"
./plugjson.py
echo
echo "TEXT Output - plugpower.py:"
./plugpower.py