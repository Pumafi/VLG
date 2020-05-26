import sys
import os
import igraph as ig
import numpy as np

def check_version_ig() -> int:
    if not ig.__version__.startswith("0.8"):
        print("Version of python-igraph superior to 0.80.0 required for Leiden Algorithm")
        return 0
    return 1


def get_bfs(g: ig.Graph, root: str = "zero", center = -1) -> list:
    if root == 'zero':
        vid = 0
    elif root == 'center':
        if center == -1:
            print("Error: no center provided.")
            exit(1)
        else:
            vid = center
    elif root == 'maxdegree': #look into dataframe for potentially better performances
        max_d = 0
        for v in g.vs:
            if v.degree() > max_d:
                vid = v.index
                max_d = v.degree()
    elif root == 'mindegree': #same here
        min_d = sys.maxsize
        for v in g.vs:
            if v.degree() < min_d:
                vid = v.index
                min_d = v.degree()
    elif root == 'doublesweep':
        extreme_1 = g.bfs(0)[0][-1]  #last element visited by bfs from node 0
        #extreme_2 = g.bfs(extreme_1)[0][-1]  #we could add another iteration, not sure it's useful though
        vid = extreme_1
    return g.bfs(vid)[0]


def permutation_from_bfs(bfs : list):
    perm=np.empty(len(bfs))
    print("started creating the permutation list from bfs list")
    for i in range(len(bfs)):
        perm.put(bfs[i], i)
    print("finished creating the permutation list from bfs list")
    return perm.tolist()


def save_result(filepath: str, modularity: float, clusters_nb: int, time):
    # Save Result
    try:
        with open(filepath, 'a') as f:
            f.writelines("{0}, {1}, {2}\n".format(modularity, clusters_nb, time))
    except:
        print("Could not save graph file \"" + filepath + "\"")
        return


