#!/bin/python3

import igraph as ig
import numpy as np
import matplotlib.pyplot as plt


def get_bfs(g: ig.Graph, root: str = "zero", center=-1) -> list:
    # TODO REOPTIMISER CA
    # UTILISER ITER -> LOADING BAR -> PAS RECALCULER LES DEGRES A CHAQUE FOIS
    # PARCOURIR QU'UNE FOIS possible ? nope
    if root == 'zero':
        vid = 0
    elif root == 'center':
        if center == -1:
            print("Error: no center provided with random graphs. Using node zero instead.")
            vid = 0
        else:
            vid = center
    elif root == 'maxdegree':
        max_d = g.maxdegree()
        for v in g.vs:
            if v.degree() == max_d:
                vid = v.index
                break
    elif root == 'mindegree':
        min_d = g.mindegree()
        for v in g.vs:
            if v.degree() == min_d:
                vid = v.index
                break
    elif root == 'doublesweep':  # TODO
        vid = 0
        print("ERRROR: doublesweep root choice is not yet implemented.")
    return g.bfs(vid)[0]


# GRAPH INFOS
NUMBER_GRAPHS = 50
SIZE_GRAPHS = 10000

# RANDOMIZE ALGO INFOS
# Geometric Random Graph
GRG = 'GRG'
LOW_VALUE_DENSITY = 0.001  # Same as the step
HIGH_VALUE_DENSITY = 0.05
# Random Growing Game
RGG = 'RGG'
LOW_VALUE_EDGES_NB = 1
HIGH_VALUE_EDGE_NB = 10
# Used one
ALGO = RGG


def main():
    mean_original_modularity = []
    mean_original_clusters = []

    mean_new_modularity = []
    mean_new_clusters = []

    mean_edges_number = []

    if ALGO == GRG:
        edge_densities = np.arange(LOW_VALUE_DENSITY, HIGH_VALUE_DENSITY, LOW_VALUE_DENSITY)
    else:
        edge_densities = np.arange(LOW_VALUE_EDGES_NB, HIGH_VALUE_EDGE_NB, LOW_VALUE_EDGES_NB)

    for edge_density in edge_densities:
        original_modularities = []
        original_clusters = []

        new_modularities = []
        new_clusters = []

        edges_nb = []

        for i in range(NUMBER_GRAPHS):
            if ALGO == GRG:
                g = ig.Graph.GRG(SIZE_GRAPHS, edge_density)
            else:
                g = ig.Graph.Growing_Random(SIZE_GRAPHS, edge_density + 1)

            clusters = g.community_leiden(objective_function="modularity")
            original_modularities.append(clusters.modularity)
            original_clusters.append(len(clusters))

            bfs = get_bfs(g)
            new_graph = g.permute_vertices(bfs)
            new_clusters_nb = new_graph.community_leiden(objective_function="modularity")
            new_modularities.append(new_clusters_nb.modularity)
            new_clusters.append(len(new_clusters_nb))

            edges_nb.append(len(g.es))

        mean_original_modularity.append(np.array(original_modularities).mean())
        mean_original_clusters.append(np.array(original_clusters).mean())

        mean_new_modularity.append(np.array(new_modularities).mean())
        mean_new_clusters.append(np.array(new_clusters).mean())

        mean_edges_number.append(np.array(edges_nb).mean())




    if ALGO == RGG:
        title = '({0} Randomized Growing Graphs ({1} nodes) for each value)'.format(NUMBER_GRAPHS, SIZE_GRAPHS)
        xlabel = "Number of Edges per Nodes"
    else:
        title = '({0} Geometric Randomized Graphs ({1} nodes) for each value)'.format(NUMBER_GRAPHS, SIZE_GRAPHS)
        xlabel = "Geometric Threshold"

    fig = plt.figure()
    # Titles
    fig.suptitle(title)
    legend_dict = {'Original': 'green', 'Reordered': 'red'}

    plt.subplot(2, 2, 1)
    plt.plot(edge_densities, mean_original_modularity, c='green')
    plt.plot(edge_densities, mean_new_modularity, c='red')
    plt.legend(legend_dict)
    plt.xlabel(xlabel)
    plt.ylabel("Mean modularity")

    plt.subplot(2, 2, 2)
    plt.plot(edge_densities, mean_original_clusters, c='green')
    plt.plot(edge_densities, mean_new_clusters, c='red')
    plt.xlabel(xlabel)
    plt.ylabel("Mean number of clusters")

    plt.subplot(2, 2, 3)
    plt.plot(mean_edges_number, mean_original_modularity, c='green')
    plt.plot(mean_edges_number, mean_new_modularity, c='red')
    plt.legend(legend_dict)
    plt.xlabel("Mean number of Edges")
    plt.ylabel("Mean modularity")

    plt.subplot(2, 2, 4)
    plt.plot(mean_edges_number, mean_original_clusters, c='green')
    plt.plot(mean_edges_number, mean_new_clusters, c='red')
    plt.xlabel("Mean number of Edges")
    plt.ylabel("Mean number of clusters")



    # plt.legend(legend_dict)

    plt.show()


main()
