#!/bin/sh

echo Testing with inet without reordering
python3 ./src/main.py ./data/inet noreorder
echo Testing with inet reordering from root zero
python3 ./src/main.py ./data/inet zero
#echo Testing with inet reordering from center 
#python3 ./src/main.py ./data/inet center
#echo Testing with inet reordering from root with mindegree
#python3 ./src/main.py ./data/inet mindegree
#echo Testing with inet reordering from root with maxdegree
#python3 ./src/main.py ./data/inet maxdegree
#echo Testing with inet reordering from extreme root found with doublesweep
#python3 ./src/main.py ./data/inet doublesweep

#echo Testing with ip TODO
#echo Testing with p2p TODO
#echo Testing with web TODO
