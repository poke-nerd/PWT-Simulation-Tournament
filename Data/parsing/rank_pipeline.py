import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def run_full_ranking_pipeline(stats_path="master_trainer_stats.csv"):
    df = pd.read_csv(stats_path)

    # Step 1: Bradley-Terry is assumed already run — AbilityScore already exists

    # Step 2: Add Tier using KMeans on AbilityScore
    scores = df['AbilityScore'].values.reshape(-1, 1)
    best_k = 0
    best_score = -1
    for k in range(2, 9):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(scores)
        sil_score = silhouette_score(scores, labels)
        if sil_score > best_score:
            best_score = sil_score
            best_k = k
            best_labels = labels

    df['Cluster'] = best_labels
    centroids = KMeans(n_clusters=best_k, random_state=42, n_init=10).fit(scores).cluster_centers_.flatten()
    cluster_to_rank = {
        cluster: rank for cluster, rank in
        zip(np.argsort(-centroids), list("SABCDEFGHIJKL")[:best_k])
    }
    df['Tier'] = df['Cluster'].map(cluster_to_rank)
    df.drop(columns=["Cluster"], inplace=True)

    # Step 3: Add Elo score
    df['Elo'] = (1500 + df['AbilityScore'] * 12).round().astype(int)

    # Overwrite master_trainer_stats.csv
    df_sorted = df.sort_values(by='Elo', ascending=False)
    df_sorted.to_csv(stats_path, index=False)
    print(f"✅ Updated {stats_path} with Tier and Elo.")


