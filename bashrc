#!/bin/bash 

if [ -n "$ZSH_VERSION" ]; then
    export IUTILS_PATH="$( cd "$( dirname "${(%):-%N}" )" && pwd )"
else
    export IUTILS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
fi

export PYTHONPATH="$IUTILS_PATH/python:$PYTHONPATH"
export PATH="$IUTILS_PATH/bin:$PATH"

RELEASE_PATH="$IUTILS_PATH/build"
export LD_LIBRARY_PATH="$RELEASE_PATH/lib:$LD_LIBRARY_PATH"

