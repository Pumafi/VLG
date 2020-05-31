# VLG


###SETUP
Go to: http://data.complexnetworks.fr/Diameter/
Download any number of those graphs
Don't extract the .gz files
Instead, put them in the data/ folder
For each graph, you should have a .meta file containing:
    - first line: number of nodes of the greatest connected component
    - second line: index of the center of the greatest connected component
        -> Example: for a graph originally named inet.gz, this file should be called inet.meta
For each of them, run from the root of the Git repository: ./process data/inet  (in this example, with inet.gz)
    -> DO NOT run: ./process data/inet.gz
When it's done, you need to update the inet.meta file:
    - the graph now has less node, since it's now only composed of its giant connected component
    - the center has a new index after shuffling
Now, for each graph, run: ./reorder.sh data/inet
Finally, you can run: ./lazy_test.sh


###RESULTS
Please note: for a graph "graphname" and a reordering method "methodname",
"graphname_noreorder" is the shuffled graph and
"graphname-methodname_noreorder" is the graph reordered with the method "methodname".
This is due to the facts that the Python script running the Leiden algorithm has the ability to reorder
the input graph itself, but we use it with already reordered graphs (for performance reasons).

###VIZUALISATION
You can use vizualize.sh to compute and see the plots for graphs inet and ip. You can also use ./compute_all_stats.sh to see the corresponding numbers.
