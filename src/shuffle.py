#!/usr/bin/python3

import sys
import os
import igraph as ig
import timeit
import numpy as np
from random import shuffle
from include import check_version_ig, get_bfs, permutation_from_bfs, read_metadata


def main() -> None:
    main_start_time = timeit.default_timer()
    check_version_ig()

    if len(sys.argv) < 2: #not enough args
        print("ERROR: need to specify graph file path.") 
        exit(1)

    else: #read graph using provided graph file path

        #get CLI parameters
        filepath = sys.argv[1]
        try:
            with open(filepath) as f:
                g = ig.Graph.Read_Edgelist(f, directed=False)
                print("Graph currently has", g.vcount(), "vertices and", g.ecount(), "edges.")
        except:
            print("Could not parse graph file \"" + filepath + "\"")
            exit(1)

    n_nodes, center = read_metadata(filepath)
    if n_nodes != g.vcount():
        print("Warning: node count in metadata doesn't match with observed node count.")

    #inform on number of nodes with degree 0
    vdz = 0
    for v in g.vs():
        if v.degree() == 0:
            vdz += 1
    print("There are", vdz, "nodes with degree 0.")
  
    permutation = list(range(g.vcount()))
    shuffle(permutation)
    g = g.permute_vertices(permutation)

    g.save(filepath + "-shuffled", format="edgelist")
    print("The shuffled graph's node count is", g.vcount())
    print("The shuffled graph's edge count is", g.ecount())
    print("The NEW CENTER'S INDEX is:", permutation[center])
    print("PLEASE, update this index in your .meta file!")
    print("Total time for shuffle.py:", "{:.2f}".format(timeit.default_timer() - main_start_time))

main()
