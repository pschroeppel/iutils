#!/bin/bash 

IMETRICS_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHONPATH="$IMETRICS_PATH/python:$PYTHONPATH"
export PATH="$IMETRICS_PATH/bin:$PATH" 

