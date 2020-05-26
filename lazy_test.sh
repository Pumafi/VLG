#!/bin/bash

if [ $OSTYPE = "linux-gnu" ]
then
        p='python3'
else
	p='python'
fi

script='./src/main.py'
n_iteration=1

for graph in './data/inet' #'./data/ip' './data/p2p' './data/web'
do
    echo
    echo -----------------$graph-----------------
    echo '1) with graph not reordered'
    $p $script $graph noreorder $n_iteration
    echo '2) with graph reordered from node zero'
    $p $script $graph-zero noreorder $n_iteration
    echo '3) with graph reordered from center' 
    $p $script $graph-center noreorder $n_iteration
    echo '4) with graph reordered from node with mindegree'
    $p $script $graph-mindegree noreorder $n_iteration
    echo '5) with graph reordered from node with maxdegree'
    $p $script $graph-maxdegree noreorder $n_iteration
    echo '6) with graph reordered from extreme node found with doublesweep'
    $p $script $graph-doublesweep noreorder $n_iteration
    echo
done
