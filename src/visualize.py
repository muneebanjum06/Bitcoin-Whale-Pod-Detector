import networkx as nx
import plotly.graph_objects as go


def draw_graph(G, centrality_df=None):

    if G.number_of_nodes() == 0:
        return None

    # ---------------- LAYOUT ----------------
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    # ---------------- CENTRALITY MAP ----------------
    pagerank = {}

    if centrality_df is not None and not centrality_df.empty:
        pagerank = dict(zip(
            centrality_df["node"],
            centrality_df["pagerank"]
        ))

    # ---------------- EDGES ----------------
    edge_x = []
    edge_y = []

    for e in G.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]

        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=0.5, color="#bbb"),
        hoverinfo="none"
    )

    # ---------------- NODE GROUPS ----------------
    groups = {
        "High Importance": {"x": [], "y": [], "text": [], "size": []},
        "Medium Importance": {"x": [], "y": [], "text": [], "size": []},
        "Low Importance": {"x": [], "y": [], "text": [], "size": []},
    }

    colors = {
        "High Importance": "red",
        "Medium Importance": "orange",
        "Low Importance": "blue"
    }

    # ---------------- NODE PROCESSING ----------------
    for node in G.nodes():

        x, y = pos[node]
        pr = pagerank.get(node, 0)
        deg = G.degree(node)

        text = f"{node[:10]}...<br>Degree: {deg}<br>PageRank: {round(pr, 6)}"

        # ---------------- CLASSIFICATION ----------------
        if pr > 0.01:
            group = "High Importance"
            size = 20
        elif pr > 0.001:
            group = "Medium Importance"
            size = 12
        else:
            group = "Low Importance"
            size = 6

        groups[group]["x"].append(x)
        groups[group]["y"].append(y)
        groups[group]["text"].append(text)
        groups[group]["size"].append(size)

    # ---------------- BUILD TRACES ----------------
    node_traces = []

    for name, g in groups.items():

        node_traces.append(
            go.Scatter(
                x=g["x"],
                y=g["y"],
                mode="markers",
                name=name,
                text=g["text"],
                hoverinfo="text",
                marker=dict(
                    size=g["size"],
                    color=colors[name],
                    line=dict(width=1)
                )
            )
        )

    # ---------------- FIGURE ----------------
    fig = go.Figure(
        data=[edge_trace] + node_traces,
        layout=go.Layout(
            title="Bitcoin Network (Centrality-Based Whale Analysis)",
            showlegend=True,
            hovermode="closest",
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )

    return fig