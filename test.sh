#!/bin/sh


echo Testing with inet, without reordering
python3 ./src/main.py ./data/inet noreorder
echo Testing with inet, reordering from root zero
python3 ./src/main.py ./data/inet zero
echo Testing with ip, without reordering
python3 ./src/main.py ./data/ip noreorder
echo Testing with ip, reordering from root zero
python3 ./src/main.py ./data/ip zero
echo Testing with p2p, without reordering
python3 ./src/main.py ./data/p2p noreorder
echo Testing with p2p, reordering from root zero
python3 ./src/main.py ./data/p2p zero
echo Testing with web, without reordering
python3 ./src/main.py ./data/web noreorder
echo Testing with web, reordering from root zero
python3 ./src/main.py ./data/web zero


#OTHER ROOT CHOICES

#echo Testing with inet reordering from center 
#python3 ./src/main.py ./data/inet center
#echo Testing with inet reordering from root with mindegree
#python3 ./src/main.py ./data/inet mindegree
#echo Testing with inet reordering from root with maxdegree
#python3 ./src/main.py ./data/inet maxdegree
#echo Testing with inet reordering from extreme root found with doublesweep
#python3 ./src/main.py ./data/inet doublesweep
