#!/usr/bin/python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats

SHOW_STD_DEV = ["Running time"]
SKIP_SHUFFLED = False


class style:
    insist = '\033[1m\033[4m'
    normal = '\033[0m'


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m = np.mean(a)
    se = scipy.stats.sem(a)
    print("Standard error of the mean:", se)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    print("Radius of the interval at 95% confidence:", h)
    return m - h, m + h


def read_result_file(filepath, all_graphs_lines, reordering):
    with open(filepath) as f:
        lines = f.readlines()
        if len(lines) < 1:
            print("Error: no lines in file.")
            exit(1)
        all_graphs_lines.append([[float(value) for value in line.split(", ")] for line in lines])
        reordering.append(filepath.split("/")[-1].split("_")[0])




def main() -> None:
    if len(sys.argv) < 2:
        print("Please indicate a result folder.")
        exit(1)

    folderpath = sys.argv[1]
    graphs_filespaths = [os.path.join(folderpath, file) for file in os.listdir(folderpath)]
    all_graphs_lines = []
    reordering = []
    kept_as_last = None
    for _, filepath in enumerate(graphs_filespaths):
        if "-" not in filepath: #this is the shuffled graph
            if SKIP_SHUFFLED: 
                continue
            else:
                kept_as_last = filepath
        else: 
            read_result_file(filepath, all_graphs_lines, reordering)
        """
        with open(filepath) as f:
            lines = f.readlines()
            if len(lines) < 1:
                print("Error: no lines in file.")
                exit(1)
            all_graphs_lines.append([[float(value) for value in line.split(", ")] for line in lines])
            reordering.append(filepath.split("/")[-1].split("_")[0])
        """
    if kept_as_last:
        read_result_file(kept_as_last, all_graphs_lines, reordering)

    all_graphs_lines = np.array(all_graphs_lines)

    #print(all_graphs_lines.shape)
    graph_count = len(reordering)
    colors = ["red", "green", "yellow", "pink", "blue", "orange", "black"]
    legend = dict(zip(reordering, colors))
    data_type_labels = ["Modularity", "Number of clusters", "Running time"]

    for data_type_idx in range(len(data_type_labels)):    
        for i in range(graph_count):
            data = all_graphs_lines[i, :, data_type_idx]
            plt.xlabel(data_type_labels[data_type_idx])
            sns.distplot(data, hist=False, rug=True, color=colors[i])
        plt.legend(legend)
        plt.show()

    for data_type_idx in range(len(data_type_labels)):    
        for i in range(graph_count):
            data = all_graphs_lines[i, :, data_type_idx]
            print(style.insist + "File name:" + style.normal + " " + reordering[i]) 
            print(data_type_labels[data_type_idx])
            mean = np.mean(data)
            print("Sample count:", data.size)
            print("Mean:", mean)
            print("Standard deviation:", np.std(data))
            if data_type_labels[data_type_idx] in SHOW_STD_DEV:
                min95, max95 = mean_confidence_interval(data)
                plt.plot([mean, mean], [0, 1 + i/graph_count], color=colors[i])
                plt.fill_betweenx([0, 1 + i/graph_count], min95, max95, color=colors[i], alpha=.3)
        if data_type_labels[data_type_idx] in SHOW_STD_DEV:
            plt.legend(legend)
            plt.show()
        
    
main()
