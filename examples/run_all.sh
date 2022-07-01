#!/bin/bash 

rm out_* -rf 

for file in *.py; do 
	echo Running $file; 
	./$file > /dev/null; 
done
