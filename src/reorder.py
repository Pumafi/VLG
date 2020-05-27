#!/usr/bin/python

import sys
import os
import igraph as ig
import timeit
from include import check_version_ig, get_bfs, permutation_from_bfs, read_metadata


def main() -> None:
    main_start_time = timeit.default_timer()
    check_version_ig()

    if len(sys.argv) < 3: #not enough args
        print("ERROR: need to specify graph and starting node for reordering.")
        print("First argument: path to graph file.")
        print("Second argument: the starting node for the BFS.")
        print("Choices are: \"zero\", \"center\", \"mindegree\", \"maxdegree\", \"doublesweep\", \"triplesweep\".")
        
        exit(1)
    else: #read graph using provided graph file path

        #get CLI parameters
        filepath = sys.argv[1]
        if sys.argv[2] in ["zero", "center", "mindegree", "maxdegree", "doublesweep", "triplesweep"]:
            root = sys.argv[2]
        else:
            print("Error: root", sys.argv[2], "not recognized.")
            exit(1)
        
        try:
            with open(filepath) as f:
                g = ig.Graph.Read_Edgelist(f, directed=False)
                print("Graph has", g.vcount(), "vertices and", g.ecount(), "edges.")
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

    #reorder and save 
    bfs = get_bfs(g, root, center)
    new_graph = g.permute_vertices(permutation_from_bfs(bfs))
    new_graph.save(filepath + "-" + root, format="edgelist")

    print("Total time for reorder.py:", "{:.2f}".format(timeit.default_timer() - main_start_time))

main()
