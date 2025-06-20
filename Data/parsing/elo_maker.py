import pandas as pd

def apply_elo(input_path="trainer_ranked_tiers.csv", output_path="trainer_ranked_tiers_elo.csv"):
    df = pd.read_csv(input_path)

    # Apply Elo formula
    df['Elo'] = 1500 + (df['AbilityScore'] * 1).round().astype(int)

    # Sort by Elo descending
    df_sorted = df.sort_values(by='Elo', ascending=False)

    # Save to new file
    df_sorted.to_csv(output_path, index=False)
    print(f"Elo ratings saved to {output_path}")

if __name__ == "__main__":
    apply_elo()

