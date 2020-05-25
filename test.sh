#!/bin/sh

if [ $OSTYPE = "linux-gnu" ]
then
        p='python3'
else
		p='python'
fi

echo Testing with inet, without reordering
$p ./src/main.py ./data/inet noreorder
echo Testing with inet, reordering from root zero
$p ./src/main.py ./data/inet zero
echo Testing with ip, without reordering
$p ./src/main.py ./data/ip noreorder
echo Testing with ip, reordering from root zero
$p ./src/main.py ./data/ip zero
echo Testing with p2p, without reordering
$p ./src/main.py ./data/p2p noreorder
echo Testing with p2p, reordering from root zero
$p ./src/main.py ./data/p2p zero
echo Testing with web, without reordering
$p ./src/main.py ./data/web noreorder
echo Testing with web, reordering from root zero
$p ./src/main.py ./data/web zero


#OTHER ROOT CHOICES

#echo Testing with inet reordering from center 
#$p ./src/main.py ./data/inet center
#echo Testing with inet reordering from root with mindegree
#$p ./src/main.py ./data/inet mindegree
#echo Testing with inet reordering from root with maxdegree
#$p ./src/main.py ./data/inet maxdegree
#echo Testing with inet reordering from extreme root found with doublesweep
#$p ./src/main.py ./data/inet doublesweep
