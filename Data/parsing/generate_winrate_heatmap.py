import pandas as pd
import plotly.express as px

def generate_winrate_heatmap(
    input_path="master_battle_matrix_wins.csv",
    stats_path="master_trainer_stats.csv",
    output_path="trainer_winrate_heatmap.html"
):
    # Load and sanitize the win matrix
    df = pd.read_csv(input_path, index_col=0)
    df.columns = df.columns.str.strip()
    df.index = df.index.str.strip()
    df = df.apply(pd.to_numeric, errors='coerce')

    # Load and sort Elo rankings
    stats_df = pd.read_csv(stats_path)
    stats_df['Trainer'] = stats_df['Trainer'].str.strip()
    if 'Elo' not in stats_df.columns:
        raise ValueError("Elo column not found in master_trainer_stats.csv")

    ordered_trainers = stats_df.sort_values(by='Elo', ascending=False)['Trainer'].tolist()

    # Reindex the matrix based on Elo order
    df = df.reindex(index=ordered_trainers, columns=ordered_trainers)

    # Print basic structure
    print("✅ Matrix loaded and reordered by Elo.")
    print("Shape:", df.shape)
    print("Top trainers:", ordered_trainers[:5])

    # Abort if matrix is empty
    if df.isna().all().all():
        print("❌ Matrix is entirely NaN. Aborting heatmap generation.")
        return

    # Create Plotly heatmap
    fig = px.imshow(
        df,
        labels=dict(x="Opponent", y="Trainer", color="Win Count"),
        title="Trainer vs Trainer Win Count Heatmap (Sorted by Elo)",
        color_continuous_scale="RdBu",
        zmin=0, zmax=df.max().max()
    )
    fig.update_layout(
        xaxis=dict(tickmode='array', tickvals=list(range(len(ordered_trainers))), ticktext=ordered_trainers),
        yaxis=dict(tickmode='array', tickvals=list(range(len(ordered_trainers))), ticktext=ordered_trainers),
        autosize=True,
        width=1000,
        height=800
    )

    # Show the figure in the browser
    fig.show()

    # Save the interactive heatmap as an HTML file
    fig.write_html(output_path)
    print(f"✅ Interactive heatmap saved to {output_path}")

if __name__ == "__main__":
    generate_winrate_heatmap()

