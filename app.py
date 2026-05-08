import streamlit as st

from src.api import fetch_btc_transactions
from src.graph_builder import build_graph
from src.whale_detector import detect_whales
from src.community_detector import detect_communities
from src.ml_cluster import create_features, cluster
from src.visualize import draw_graph
from src.centrality import compute_centrality

st.set_page_config(layout="wide")

st.title("🐋 Bitcoin Whale Pod Detection Dashboard")

# ---------------- SIDEBAR ----------------
limit_blocks = st.sidebar.slider("Blocks to Fetch", 1, 10, 3)
whale_threshold = st.sidebar.number_input("Whale Threshold (BTC)", 5.0)

# ---------------- RUN ----------------
if st.button("Run Analysis"):

    st.info("Fetching blockchain data...")
    data = fetch_btc_transactions(limit_blocks)

    if isinstance(data, dict) and "error" in data:
        st.error(data["error"])
        st.stop()

    st.info("Building graph...")
    G = build_graph(data)

    st.success(f"Nodes: {len(G.nodes())} | Edges: {len(G.edges())}")

    # ---------------- DASHBOARD METRICS ----------------
    st.subheader("📊 Network Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Nodes", len(G.nodes()))
    col2.metric("Edges", len(G.edges()))

    avg_deg = (
        sum(dict(G.degree()).values()) / len(G.nodes())
        if len(G.nodes()) > 0 else 0
    )

    col3.metric("Avg Degree", round(avg_deg, 2))

    # ---------------- CENTRALITY ----------------
    st.subheader("🧠 Centrality Analysis")

    centrality_df = compute_centrality(G)

    if not centrality_df.empty:

        top = centrality_df.sort_values("pagerank", ascending=False).head(10)

        st.write("🔥 Top 10 Important Wallets (PageRank)")
        st.dataframe(top)

    else:
        st.warning("No centrality data available")

    # ---------------- GRAPH ----------------
    st.subheader("🕸 Interactive Transaction Graph")

    fig = draw_graph(G, centrality_df)

    if fig:
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- WHALES ----------------
    st.subheader("🐋 Whale Wallets")

    whales = detect_whales(G, whale_threshold)
    st.write(whales)

    # ---------------- COMMUNITIES ----------------
    st.subheader("🌊 Whale Pods")

    communities = detect_communities(G)
    st.write(communities)

    # ---------------- ML CLUSTERING ----------------
    st.subheader("🤖 ML Clusters")

    df = create_features(G)
    st.write(cluster(df))