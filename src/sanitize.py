#!/usr/bin/python3

import sys
import os
import igraph as ig
import timeit
import numpy as np
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

    n_nodes, _ = read_metadata(filepath)
    if n_nodes != g.vcount():
        print("Error: node count in metadata doesn't match with observed node count. Maybe this graph has already been sanitized?")
        exit(1)

    #inform on number of nodes with degree 0
    vdz = 0
    for v in g.vs():
        if v.degree() == 0:
            vdz += 1
    print("There are", vdz, "nodes with degree 0.")


    # wanted to compute the giant connected component, but there are functions for that
    """
    bfs = g.bfs(0)
    visited = bfs[0]
    parent = bfs[2]
    marked = np.zeros(len(bfs))
    components = []
    for i in reversed(range(len(visited))):
        if marked[i]:
            continue
        component = []

        components = []
    """ 
    # here they are
    component_clustering = g.components()
    components = component_clustering.subgraphs()
    print("Found strong components with the following node counts:")
    print([c.vcount() for c in components])
    g = component_clustering.giant()


    g.save(filepath + "-SANITIZED", format="edgelist")
    print("The sanitized graph's node count is",
            str(g.vcount()) + ", please update the metadata file accordingly.") 

    print("Total time for sanitize.py:", "{:.2f}".format(timeit.default_timer() - main_start_time))

main()
