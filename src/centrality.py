import networkx as nx
import pandas as pd

def compute_centrality(G):

    if G.number_of_nodes() == 0:
        return pd.DataFrame()

    degree_c = nx.degree_centrality(G)
    betweenness_c = nx.betweenness_centrality(G)
    pagerank_c = nx.pagerank(G)

    data = []

    for node in G.nodes():

        data.append([
            node,
            degree_c.get(node, 0),
            betweenness_c.get(node, 0),
            pagerank_c.get(node, 0)
        ])

    df = pd.DataFrame(data, columns=[
        "node",
        "degree_centrality",
        "betweenness_centrality",
        "pagerank"
    ])

    return df