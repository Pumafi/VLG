#!/usr/bin/python

import sys
import os
import igraph as ig
import timeit
from include import check_version_ig, get_bfs, permutation_from_bfs, save_result, read_metadata


def main() -> None:
    main_start_time = timeit.default_timer()
    check_version_ig()

    if len(sys.argv) < 3: #not enough args
        print("ERROR: need to specify graph and starting node for reordering (optionally, the number of iterations).")
        print("First argument: path to graph file.")
        print("Second argument: \"noreorder\" if not reordering, else the starting node for the BFS.")
        print("Choices are: \"noreorder\", \"zero\", \"center\", \"mindegree\", \"maxdegree\", \"doublesweep\", \"triplesweep\".")
        print("Third argument (optional): number of iterations for benchmarking purposes.")
        exit(1)

    #get CLI parameters
    filepath = sys.argv[1]
    if sys.argv[2] in ["noreorder", "zero", "center", "mindegree", "maxdegree", "doublesweep", "triplesweep"]:
        root = sys.argv[2]
    else:
        print("Error: root", sys.argv[2], "not recognized.")
        exit(1)
    
    n_iteration = 1
    if len(sys.argv) == 4:
        try:
            n_iteration = int(sys.argv[3])
            if n_iteration < 1:
                raise Exception
        except:
            print("Third parameter (number of iterations) should be a positive integer.")
            exit(1)

    #read graph using provided graph file path
    try:
        with open(filepath) as f:
            g = ig.Graph.Read_Edgelist(f, directed=False)
            #g = ig.Graph.Read(f, format='edgelist')
            print("Graph", filepath, "has", g.vcount(), "vertices and", g.ecount(), "edges.")
    except:
        print("Could not parse graph file \"" + filepath + "\"")
        exit(1)

    n_nodes, center = read_metadata(filepath)
    if center == -1 and root == "center":
        print("Error: center not found in metadata.")
        exit(1)
    if n_nodes != g.vcount():
        print("Error: node count in metadata doesn't match with observed node count.")
        exit(1)

    # Reorder or not, then benchmark the Leiden algorithm
    
    if root == "noreorder":
        new_graph = g
    else:
        bfs = get_bfs(g, root, center)
        new_graph = g.permute_vertices(permutation_from_bfs(bfs))

    for i in range(n_iteration):
        start_time = timeit.default_timer()
        new_clusters = new_graph.community_leiden(objective_function="modularity")
        time = timeit.default_timer() - start_time
        print("Elapsed time during Leiden algorithm:", "{:.2f}".format(time))
        print("Graph: modularity = {0:.4f}, number of clusters: {1}".format(new_clusters.modularity, len(new_clusters)))
        save_result("results/" + filepath + "_" + root, new_clusters.modularity, len(new_clusters), time)

    print("Total time for main function:", "{:.2f}".format(timeit.default_timer() - main_start_time))


main()
