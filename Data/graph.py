import pandas as pd
import plotly.express as px

# Load the CSV file
file_path = '/home/gonzalez/Pokemon-Simulator/Data/master_trainer_stats.csv'  # Path to your CSV file
df = pd.read_csv(file_path)

# Add 50 to negative AbilityScore values
df['AbilityScore'] = df['AbilityScore'].apply(lambda x: x + 50 if x < 0 else x)

# Example: Assume the dataset has a 'Region' column
# You might need to replace 'Region' with the actual column in your dataset

# Create a 3D Scatter Plot using Plotly
fig = px.scatter_3d(df, x="wins", y="losses", z="Elo", color="Tier",
                    title="3D Scatter Plot of Wins, Losses, and Elo",
                    labels={"Wins": "Number of Wins", "Losses": "Number of Losses", "Elo": "Elo Score", "Tier": "Trainer Tier"})

# Show the plot
fig.show()
