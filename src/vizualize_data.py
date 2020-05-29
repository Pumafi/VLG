#!/usr/bin/python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main() -> None:
    if len(sys.argv) < 2:
        print("Please indicate a result file.")
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

    for i in range(len(reordering)):
        modularities = all_graphs_lines[i, :, 0]
        clusters_nb = all_graphs_lines[i, :, 1]
        times = all_graphs_lines[i, :, 2]
        plt.subplot(3, 1, 1)
        plt.xlabel("Running time")
        sns.distplot(times, hist=False, rug=True, color=colors[i])
        plt.subplot(3, 1, 2)
        plt.xlabel("Number of clusters")
        sns.distplot(clusters_nb, hist=False, rug=True, color=colors[i])
        plt.subplot(3, 1, 3)
        plt.xlabel("Modularity")
        sns.distplot(modularities, hist=False, rug=True, color=colors[i])

    plt.legend(legend)
    plt.show()


main()
