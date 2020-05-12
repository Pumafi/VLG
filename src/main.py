import igraph as ig
from fa2 import ForceAtlas2
import cairocffi


def check_version_ig() -> int:
    if not ig.__version__.startswith("0.8"):
        print("Version of python-igraph superior to 0.80.0 required for Leiden Algorithm")
        return 0
    return 1


def config_fa2() -> ForceAtlas2:
    # Create ForceAtlas2 object with desired parameters
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=2.0,
        strongGravityMode=False,
        gravity=0.1,

        # Log
        verbose=True)

    return forceatlas2


def adjust_weights(g: ig.Graph, clusters: ig.VertexClustering, weight_in=10.0, weight_between=1.0) -> list:
    edges = g.get_edgelist()
    membership = clusters.membership
    weights = list(map(lambda e: weight_in if membership[e[0]] == membership[e[1]] else weight_between, edges))
    return weights


def get_bfs(g: ig.Graph, root: str = "zero") -> list:
    # TODO REOPTIMISER CA
    # UTILISER ITER -> LOADING BAR -> PAS RECALCULER LES DEGRES A CHAQUE FOIS
    # PARCOURIR QU'UNE FOIS possible ? nope
    if root == 'zero':
        vid = 0
    elif root == 'center':
        vid = 0
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
    return g.bfs(vid)[0]


def draw_clustered_graph_fa2(g: ig.Graph, clusters: ig.VertexClustering):
    forceatlas2 = config_fa2()
    pal = ig.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    g.es['weight'] = adjust_weights(g, clusters, 100, 10)
    layout = forceatlas2.forceatlas2_igraph_layout(g, pos=None, iterations=100, weight_attr='weight')
    #layout = g.layout_drl()
    ig.plot(g, layout=layout, bbox=(1000, 1000), margin=10, vertex_frame_width=0, palette=pal, mark_groups=clusters)


def main(filepath: str, random_graph=True) -> None:
    check_version_ig()

    # Read Graph
    if random_graph:
        g = ig.Graph.GRG(1000, 0.1)
    elif len(filepath) > 0:
        g = ig.Graph.Read_GML(filepath)
    else:
        print("Need a filepath or activate random graph generation")
        return


    # Apply Leiden algorithm
    clusters = g.community_leiden(objective_function="modularity")
    print("Graph: Modularity = {0}, Number of Clusters: {1}".format(clusters.modularity, len(clusters)))

    draw_clustered_graph_fa2(g, clusters)

    bfs = get_bfs(g, "zero")
    new_graph = g.permute_vertices(bfs)
    new_clusters = new_graph.community_leiden(objective_function="modularity")
    print("Reord. Graph: Modularity = {0}, Number of Clusters: {1}".format(new_clusters.modularity, len(new_clusters)))


main("../data/netscience.gml")
