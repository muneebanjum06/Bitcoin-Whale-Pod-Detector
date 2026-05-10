import community


def detect_communities(G):
    """
    Runs Louvain community detection on the undirected version of the graph.
    Returns a dict: {wallet_address: community_id}
    """
    if G.number_of_nodes() == 0:
        return {}

    return community.best_partition(G.to_undirected())


def detect_whale_pods(G, partition, whale_threshold=5.0):
    """
    Cross-references whale wallets with their community memberships.
    A 'whale pod' is a community that contains 2 or more whale wallets.

    Returns a list of dicts, each describing one pod:
    [
        {
            "pod_id": 3,
            "whale_count": 3,
            "total_wallets_in_community": 27,
            "whales": [
                {"wallet": "bc1q...", "total_btc_sent": 36.36},
                ...
            ]
        },
        ...
    ]
    """

    if not partition:
        return []

    # Step 1 — find whale wallets (same logic as whale_detector.py)
    whales = {}
    for node in G.nodes():
        total_sent = sum(
            G[node][n].get("weight", 0)
            for n in G.successors(node)
            if G.has_edge(node, n)
        )
        if total_sent >= whale_threshold:
            whales[node] = round(total_sent, 4)

    if not whales:
        return []

    # Step 2 — count how many wallets are in each community
    community_sizes = {}
    for wallet, community_id in partition.items():
        community_sizes[community_id] = community_sizes.get(community_id, 0) + 1

    # Step 3 — for each whale, find which community it belongs to
    community_to_whales = {}
    for whale_wallet, btc_sent in whales.items():
        community_id = partition.get(whale_wallet)
        if community_id is None:
            continue
        if community_id not in community_to_whales:
            community_to_whales[community_id] = []
        community_to_whales[community_id].append({
            "wallet": whale_wallet,
            "total_btc_sent": btc_sent
        })

    # Step 4 — a pod = community with 2 or more whales
    pods = []
    for community_id, whale_list in community_to_whales.items():
        if len(whale_list) >= 2:
            pods.append({
                "pod_id": community_id,
                "whale_count": len(whale_list),
                "total_wallets_in_community": community_sizes.get(community_id, 0),
                "whales": sorted(whale_list, key=lambda x: x["total_btc_sent"], reverse=True)
            })

    # Sort pods by whale count descending
    pods.sort(key=lambda x: x["whale_count"], reverse=True)

    return pods