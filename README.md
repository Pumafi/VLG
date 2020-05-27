# VLG

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

