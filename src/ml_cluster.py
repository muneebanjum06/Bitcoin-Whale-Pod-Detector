import networkx as nx
import pandas as pd


def create_features(G):

    if G.number_of_nodes() == 0:
        return pd.DataFrame()

    pr = nx.pagerank(G)

    data = []

    for n in G.nodes():

        data.append([
            n,
            G.degree(n),
            G.in_degree(n),
            G.out_degree(n),
            pr.get(n, 0)
        ])

    return pd.DataFrame(data, columns=["node", "deg", "in", "out", "pagerank"])
