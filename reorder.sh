#!/bin/bash

if [ $OSTYPE = "linux-gnu" ]
then
        p='python3'
else
	p='python'
fi

script='./src/reorder.py'

for graph in './data/inet' './data/ip' './data/p2p' './data/web'
do
    echo
    echo -----------------$graph-----------------
    echo '1) reordering from node zero'
    $p $script $graph zero 
    echo '2) reordering from center' 
    $p $script $graph center 
    echo '3) reordering from node with mindegree'
    $p $script $graph mindegree 
    echo '4) reordering from node with maxdegree'
    $p $script $graph maxdegree 
    echo '5) reordering from extreme node found with doublesweep'
    $p $script $graph doublesweep 
    echo '6) reordering from extreme node found with triplesweep'
    $p $script $graph triplesweep 
    echo
done
