import networkx as nx
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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

    return pd.DataFrame(data, columns=["node","deg","in","out","pagerank"])


def cluster(df):

    if df.empty:
        return df

    X = df[["deg","in","out","pagerank"]]

    X = StandardScaler().fit_transform(X)

    k = min(3, len(df))

    model = KMeans(n_clusters=k, n_init=10)
    df["cluster"] = model.fit_predict(X)

    return df