#!/bin/bash

for f in results/inet/*
do
    echo -e "\033[1m${f}\033[0m"
    ./src/mean_variance_each_column.py $f
done

for f in results/ip/*
do
    echo -e "\033[1m${f}\033[0m"
    ./src/mean_variance_each_column.py $f
done
