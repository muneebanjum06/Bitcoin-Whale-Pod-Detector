def detect_whales(G, threshold):

    whales = []

    for node in G.nodes():

        total = sum(
            G[node][n].get("weight", 0)
            for n in G.successors(node)
            if G.has_edge(node, n)
        )

        if total >= threshold:
            whales.append((node, round(total, 4)))

    return whales