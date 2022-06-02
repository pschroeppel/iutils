#!/bin/bash 

IUTILS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $IUTILS_PATH 
rm -rf build 

mkdir build 
cd build
cmake .. 
make 
