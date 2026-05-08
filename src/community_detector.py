import community

def detect_communities(G):

    if G.number_of_nodes() == 0:
        return {}

    return community.best_partition(G.to_undirected())