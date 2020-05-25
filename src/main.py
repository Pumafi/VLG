#!/usr/bin/python

import sys
import igraph as ig
import timeit


def check_version_ig() -> int:
    if not ig.__version__.startswith("0.8"):
        print("Version of python-igraph superior to 0.80.0 required for Leiden Algorithm")
        return 0
    return 1

def get_bfs(g: ig.Graph, root: str = "zero", center = -1) -> list:
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
    elif root == 'doublesweep': #TODO
        vid = 0
        print("ERRROR: doublesweep root choice is not yet implemented.")
    return g.bfs(vid)[0]


def main() -> None:
    check_version_ig()

    if len(sys.argv) < 3: #not enough args
        print("ERROR: need to specify graph and starting node for reordering (optionally, the number of iterations).")
        print("First argument: path to graph file.")
        print("Second argument: \"noreorder\" if not reordering, else the starting node for the BFS.")
        print("Choices are: \"noreorder\", \"zero\", \"center\", \"mindegree\", \"maxdegree\", \"doublesweep\".")
        print("Third argument (optional): number of iterations for benchmarking purposes.")
        
        exit(1)
    else: #read graph using provided graph file path

        #get CLI parameters
        filepath = sys.argv[1]
        if sys.argv[2] in ["noreorder", "zero", "center", "mindegree", "maxdegree", "doublesweep"]:
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

        try:
            with open(filepath) as f:
                g = ig.Graph.Read_Edgelist(f, directed=False)
                #g = ig.Graph.Read(f, format='edgelist')
                print("Graph has", g.vcount(), "vertices and", g.ecount(), "edges.")
        except:
            print("Could not parse graph file \"" + filepath + "\"")
            exit(1)

        center = -1
        if root == "center":
            try:
                with open(filepath + '.center') as f:
                    center = int(f.readlines()[0])
                    print("Center:", center)
            except Exception as e:
                print("No center file named \"" + filepath + ".center\" found.")
                exit(1)


    # Reorder or not, then benchmark the Leiden algorithm
    
    if root == "noreorder":
        new_graph = g
    else:
        bfs = get_bfs(g, root, center)
        new_graph = g.permute_vertices(bfs)

    for i in range(n_iteration):
        start_time = timeit.default_timer()
        new_clusters = new_graph.community_leiden(objective_function="modularity")
        print("Elapsed time during Leiden algorithm:", "{:.2f}".format(timeit.default_timer() - start_time))
        print("Graph: modularity = {0:.4f}, number of clusters: {1}".format(new_clusters.modularity, len(new_clusters)))

main()
