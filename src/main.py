import sys
import igraph as ig

DRAW = False

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


def main():
    check_version_ig()

    # Read Graph
    if len(sys.argv) < 3: #no args, random graph -> not anymore
        #g = ig.Graph.GRG(1000, 0.1)
        print("ERROR: need to specify graph and starting node for reordering.")
        print("Choices are: \"noreorder\", \"zero\", \"center\", \"mindegree\", \"maxdegree\", \"doublesweep\".")
        exit(1)
    else: #using provided graph file path

        #get parameters
        filepath = sys.argv[1]
        if sys.argv[2] in ["noreorder", "zero", "center", "mindegree", "maxdegree", "doublesweep"]:
            root = sys.argv[2]
        else:
            print("Error: root", sys.argv[2], "not recognized.")
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

            # Apply Leiden algorithm
    if root == "noreorder":
        clusters = g.community_leiden(objective_function="modularity")
        print("Graph: modularity = {0}, number of clusters: {1}".format(clusters.modularity, len(clusters)))
        exit(0)

    bfs = get_bfs(g, root, center)
    new_graph = g.permute_vertices(bfs)
    new_clusters = new_graph.community_leiden(objective_function="modularity")
    print("Reord. graph: modularity = {0}, number of clusters: {1}".format(new_clusters.modularity, len(new_clusters)))

main()
