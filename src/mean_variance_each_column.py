#!/usr/bin/python3

import sys
from math import sqrt
# I should use numpy but alas I'm stupid

PRINT_COLUMNS = [0, 1, 2]
COLUMN_NAMES=["modularity", "cluster", "time"]
PRINT=True

def log(header, value):
    if PRINT:
        print(header, value)
    else:
        pass #add to buffer to save to file at the end

def main() -> None:
    if len(sys.argv) < 2:
        print("Please indicate a result file.")
        exit(1)
    filepath = sys.argv[1]
    with open(filepath) as f:
        lines = f.readlines()
        if len(lines) < 1:
            print("Error: no lines in file.")
            exit(1)
        log("Number of rows:", len(lines))
    try:
        lines = [[float(value) for value in line.split(", ")] for line in lines]
    except:
        print("Error: couldn't split or convert to float.")
        exit(1)

    height=len(lines)
    width=len(lines[0])

    #checking dimensions
    for j in range(width):  # columns
        for i in range(height):  # rows (thus for each value in column)
            if len(lines[i]) != width:
                print("Error: width discrepancy at row",  i)
                exit(1)

    # computing mean for each column
    means = []
    for j in range(width):  # columns
        sum_values=0
        for i in range(height):  # rows (thus for each value in column)
            sum_values += lines[i][j]
        mean = sum_values / height
        if j in PRINT_COLUMNS:
            log("Mean for column " + COLUMN_NAMES[j] + ":", mean)
        means.append(mean)

    # computing standard deviation for each column
    stdevs = []
    for j in range(width):  # columns
        sum_squared_differences = 0
        for i in range(height):  # rows (thus for each value in column)
            difference = lines[i][j] - means[j]
            sum_squared_differences += difference ** 2
        stdev = sqrt(sum_squared_differences / height)
        if j in PRINT_COLUMNS:
            log("Standard deviation for column " + COLUMN_NAMES[j] + ": ", stdev)
        stdevs.append(stdev)
       
main()
