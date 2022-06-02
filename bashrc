#!/bin/bash 

IUTILS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHONPATH="$IUTILS_PATH/python:$PYTHONPATH"
export PATH="$IUTILS_PATH/bin:$PATH"

RELEASE_PATH="$IUTILS_PATH/build"
export LD_LIBRARY_PATH="$RELEASE_PATH/lib:$LD_LIBRARY_PATH"

