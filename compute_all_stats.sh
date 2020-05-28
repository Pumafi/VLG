#!/bin/bash

for f in results/data/*
do
    echo -e "\033[1m${f}\033[0m"
    ./src/mean_variance_each_column.py $f
done
