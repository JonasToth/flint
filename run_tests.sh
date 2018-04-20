#!/bin/sh

cd src/

sucess=0
python3 -m unittest -v test_*.py
sucess=$sucess || $?
python3 -m unittest discover -v -s format/ -p 'test_*.py'
sucess=$sucess || $?
python3 -m unittest discover -v -s check/ -p 'test_*.py'
sucess=$sucess || $?

if [ $sucess -ne 0 ]
then
    echo "Tests failed"
    exit 1
else
    echo "Tests succeeded"
fi
