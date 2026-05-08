import networkx as nx

def build_graph(data):

    G = nx.DiGraph()

    if isinstance(data, dict):
        return G

    for tx in data:

        inputs = tx.get("vin", [])
        outputs = tx.get("vout", [])

        senders = []

        for inp in inputs:
            prev = inp.get("prevout")
            if prev and prev.get("scriptpubkey_address"):
                senders.append(prev["scriptpubkey_address"])

        for out in outputs:
            receiver = out.get("scriptpubkey_address")
            value = out.get("value", 0) / 1e8

            for s in senders:
                if s and receiver:
                    G.add_edge(s, receiver, weight=value)

    return G