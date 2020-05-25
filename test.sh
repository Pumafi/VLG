#!/bin/bash

if [ $OSTYPE = "linux-gnu" ]
then
        p='python3'
else
	p='python'
fi

n_iteration=4

echo
echo
echo Testing with inet, without reordering
$p ./src/main.py ./data/inet noreorder $n_iteration
echo Testing with inet, reordering from root zero
$p ./src/main.py ./data/inet zero $n_iteration
echo
echo
echo Testing with ip, without reordering
$p ./src/main.py ./data/ip noreorder $n_iteration
echo Testing with ip, reordering from root zero
$p ./src/main.py ./data/ip zero $n_iteration
echo
echo
echo Testing with p2p, without reordering
$p ./src/main.py ./data/p2p noreorder $n_iteration
echo Testing with p2p, reordering from root zero
$p ./src/main.py ./data/p2p zero $n_iteration
echo
echo
echo Testing with web, without reordering
$p ./src/main.py ./data/web noreorder $n_iteration
echo Testing with web, reordering from root zero
$p ./src/main.py ./data/web zero $n_iteration
echo
echo


#OTHER ROOT CHOICES

#echo Testing with inet reordering from center 
#$p ./src/main.py ./data/inet center
#echo Testing with inet reordering from root with mindegree
#$p ./src/main.py ./data/inet mindegree
#echo Testing with inet reordering from root with maxdegree
#$p ./src/main.py ./data/inet maxdegree
#echo Testing with inet reordering from extreme root found with doublesweep
#$p ./src/main.py ./data/inet doublesweep
