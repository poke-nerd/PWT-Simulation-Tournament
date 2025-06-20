import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def label_ranks_from_scores(input_path="master_trainer_stats_bt_matrix.csv", output_path="trainer_ranked_tiers.csv"):
    df = pd.read_csv(input_path)
    scores = df['AbilityScore'].values.reshape(-1, 1)

    # Try clustering from 2 to 8 groups
    best_k = 0
    best_score = -1
    for k in range(2, 9):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = kmeans.fit_predict(scores)
        sil_score = silhouette_score(scores, labels)
        if sil_score > best_score:
            best_score = sil_score
            best_k = k
            best_labels = labels

    # Attach best labels
    df['Cluster'] = best_labels

    # Map cluster centroids to ranks (highest ability = best)
    centroids = KMeans(n_clusters=best_k, random_state=42, n_init=20).fit(scores).cluster_centers_.flatten()
    cluster_to_rank = {
        cluster: rank for cluster, rank in 
        zip(np.argsort(-centroids), list("SABCDEFGHIJKL")[:best_k])
    }

    df['Tier'] = df['Cluster'].map(cluster_to_rank)
    df = df.drop(columns=["Cluster"])
    df.to_csv(output_path, index=False)
    print(f"Saved trainer ranks to {output_path}")

if __name__ == "__main__":
    label_ranks_from_scores()

