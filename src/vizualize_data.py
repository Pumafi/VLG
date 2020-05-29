#!/usr/bin/python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main() -> None:
    if len(sys.argv) < 2:
        print("Please indicate a result folder.")
        exit(1)

    folderpath = sys.argv[1]
    graphs_filespaths = [os.path.join(folderpath, file) for file in os.listdir(folderpath)]
    all_graphs_lines = []
    reordering = []
    for ii, filepath in enumerate(graphs_filespaths):
        with open(filepath) as f:
            lines = f.readlines()
            if len(lines) < 1:
                print("Error: no lines in file.")
                exit(1)
            all_graphs_lines.append([[float(value) for value in line.split(", ")] for line in lines])
            reordering.append(filepath.split("/")[-1].split("_")[0])

    all_graphs_lines = np.array(all_graphs_lines)

    #print(all_graphs_lines.shape)
    colors = ["red", "green", "yellow", "pink", "blue", "orange", "black"]
    legend = dict(zip(reordering, colors))

    data_type_labels = ["Modularity", "Number of clusters", "Running time"]
    for data_type_idx in range(len(data_type_labels)):    
        for i in range(len(reordering)):
            data = all_graphs_lines[i, :, data_type_idx]
            plt.xlabel(data_type_labels[data_type_idx])
            sns.distplot(data, hist=False, rug=True, color=colors[i])
        plt.legend(legend)
        plt.show()


main()
