#!/bin/sh

echo Testing with inet at root zero
python3 ./src/main.py ./data/inet zero
echo Testing with inet at root mindegree
python3 ./src/main.py ./data/inet mindegree
echo Testing with inet at root maxdegree
python3 ./src/main.py ./data/inet maxdegree
echo Testing with ip TODO
echo Testing with p2p TODO
echo Testing with web TODO
