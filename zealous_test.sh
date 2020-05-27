#!/bin/bash

if [ $OSTYPE = "linux-gnu" ]
then
        p='python3'
else
	p='python'
fi

script='./src/main.py'
n_iteration=1

for graph in './data/inet' './data/ip' './data/p2p' './data/web'
do
    echo
    echo -----------------$graph-----------------
    echo '1) without reordering'
    $p $script $graph noreorder $n_iteration
    echo '2) reordering from root zero'
    $p $script $graph zero $n_iteration
    echo '3) reordering from center' 
    $p $script $graph center $n_iteration
    echo '4) reordering from root with mindegree'
    $p $script $graph mindegree $n_iteration
    echo '5) reordering from root with maxdegree'
    $p $script $graph maxdegree $n_iteration
    echo '6) reordering from extreme node found with doublesweep'
    $p $script $graph doublesweep $n_iteration
    echo '7) reordering from extreme node found with triplesweep'
    $p $script $graph triplesweep $n_iteration
    echo
done
