#!/bin/sh

cd src/
python3 -m unittest -v test_*.py
python3 -m unittest discover -v -s format/ -p 'test_*.py'
python3 -m unittest discover -v -s check/ -p 'test_*.py'
