# iMetrics

## Overview 

This library provides a set of image utility functions. It is a supporting library for
[iTypes](https://github.com/eddy-ilg/itypes.git) and [iViz](https://github.com/eddy-ilg/iviz). 

___Tutorials and YouTube videos will be made available in the second
half of 2022.___

## Installation 

Prerequisites: 
* Install [iTypes](https://github.com/eddy-ilg/itypes.git).

Instructions: 

    cd /my/code
    git clone https://github.com/eddy-ilg/iutils
    cd imetrics 

    # Install requirements
    pip3 install --user -r requirements.txt 

    # Compile ctypes extensions 
    # (will be kept in the local "build" folder that will be added to LD_LIBRARY_PATH)
    ./compile.sh 

    # Add to your ~/.bashrc:
    # (this will configure PATH, PYTHONPATH and LD_LIBRARY_PATH)
    source /my/code/iutils/bashrc 

## License

The code is licensed under the MIT license. Please contact [Eddy Ilg](mailto:me@eddy-ilg.net)
for questions.

## Contributions

Contributions are welcome. Please contact [Eddy Ilg](mailto:me@eddy-ilg.net)
for questions.


