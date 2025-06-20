import pandas as pd
import numpy as np
from scipy.linalg import lstsq

def run_bt_matrix(input_path="master_trainer_stats.csv", output_path=None):
    # Load CSV
    df = pd.read_csv(input_path)
    n = len(df)

    # Step 1: Build A matrix (n x n)
    A = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                A[i, j] = -1  # Off-diagonal: one match against each other trainer
        A[i, i] = n - 1     # Diagonal: total number of comparisons

    # Step 2: Build b vector (raw wins)
    b = df['wins'].values.astype(float)

    # Step 3: Add zero-mean constraint
    A_aug = np.vstack([A, np.ones(n)])
    b_aug = np.append(b, 0)

    # Step 4: Solve A·x = b using least squares
    x, _, _, _ = lstsq(A_aug, b_aug)

    # Step 5: Add scores to DataFrame and save
    df['AbilityScore'] = x
    df = df.sort_values(by='win_loss_ratio', ascending=False)

    # Overwrite by default
    if output_path is None:
        output_path = input_path

    df.to_csv(output_path, index=False)
    print(f"Saved Bradley-Terry matrix scores to {output_path}")

if __name__ == "__main__":
    run_bt_matrix()

