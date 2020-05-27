#!/bin/bash

echo 'This script will delete a given number of lines from each of the three graphs in data/.'
echo 'Do not use this script twice, otherwise the graphs will obviously be damaged.'
echo '(WARNING: this script only removes the degree information in the graph files, not the node count.'
echo 'Remove the node count yourself PRIOR to running this script.)'
read -p "Are you sure you want to delete the first N lines of each graph? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sed -i -e 1,1719037d "./data/inet"
    sed -i -e 1,2250498d "./data/ip"
fi
