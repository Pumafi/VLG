#!/bin/bash

if [ $OSTYPE = "linux-gnu" ]
then
        p='python3'
else
	p='python'
fi

path=$1

echo 'Please provide path without the .gz at the end.'
echo 'You provided the following path:'
echo $path
read -p "Ready? (y/n)" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    #extract
    gunzip "$path.gz"

    #prune nodecount + 1 lines
    read -r nodecount<$path
    sed -i -e 1,${nodecount}d $path
    sed -i -e 1,1d $path

    #sanitize
    ./src/sanitize.py $path
    mv ${path}-sanitized $path

    #shuffle
    ./src/shuffle.py $path
    mv ${path}-shuffled $path

    #do all reorders for this graph
    #./reorder.sh $path
    #DO THIS YOURSELF, AFTER HAVING FIXED THE .meta FILE!!

    echo 'The pre-processing of' $path 'is done!'
    echo 'Please update the .meta file for this graph with the values printed above.'
    echo 'Afterwards, run ./reorder.py on the graph file.'
    echo 'Finally, you will be able to execute ./lazy_test.sh'
fi
