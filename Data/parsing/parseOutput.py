import re
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap

def print_battle_matrix(battle_matrix):
    # Calculate overall wins for each trainer
    overall_wins = {}
    for trainer1 in battle_matrix:
        overall_wins[trainer1] = sum(record['wins'] for trainer2, record in battle_matrix[trainer1].items() if trainer1 != trainer2)

    # Sort trainers by overall wins in descending order
    sorted_trainers = sorted(overall_wins.keys(), key=lambda t: overall_wins[t], reverse=True)

    # Print the header row
    print(f"{'':>12}", end="")
    for trainer in sorted_trainers:
        print(f"{trainer:>12}", end="")
    print(f"{' Overall':>18}")

    # Print each row of the matrix
    for trainer1 in sorted_trainers:
        print(f"{trainer1:>12}", end="")

        overall_wins_row = overall_losses = overall_ties = 0
        for trainer2 in sorted_trainers:
            if trainer1 == trainer2:
                print(f"{'---':>12}", end="")  # Placeholder for battles against themselves
            else:
                record = battle_matrix[trainer1][trainer2]
                result_str = f"{record['wins']}W-{record['losses']}L-{record['ties']}T"
                print(f"{result_str:>12}", end="")

                # Sum up wins, losses, and ties
                overall_wins_row += record['wins']
                overall_losses += record['losses']
                overall_ties += record['ties']

        # Print the overall wins, losses, and ties
        overall_str = f"{overall_wins_row}W-{overall_losses}L-{overall_ties}T"
        print(f"{overall_str:>18}")

def parse_battles(file_path):
    trainer_stats = defaultdict(lambda: {'wins': 0, 'losses': 0, 'ties': 0})
    battle_matrix = defaultdict(lambda: defaultdict(lambda: {'wins': 0, 'losses': 0, 'ties': 0}))

    with open(file_path, 'r') as file:
        content = file.read()

    battles = re.split(r'\[\[\[\[\[|\]\]\]\]\]', content)[1:-1]
    name_pattern = re.compile(r'^(.*?) vs (.*?)\n', re.MULTILINE)

    for battle in battles:
        match = name_pattern.search(battle)
        if not match:
            continue

        bot_1, bot_2 = match.groups()

        if "|win|Bot 1" in battle:
            trainer_stats[bot_1]['wins'] += 1
            trainer_stats[bot_2]['losses'] += 1
            battle_matrix[bot_1][bot_2]['wins'] += 1
            battle_matrix[bot_2][bot_1]['losses'] += 1
        elif "|win|Bot 2" in battle:
            trainer_stats[bot_1]['losses'] += 1
            trainer_stats[bot_2]['wins'] += 1
            battle_matrix[bot_2][bot_1]['wins'] += 1
            battle_matrix[bot_1][bot_2]['losses'] += 1
        elif "|tie" in battle and "|tier" not in battle:
            trainer_stats[bot_1]['ties'] += 1
            trainer_stats[bot_2]['ties'] += 1
            battle_matrix[bot_1][bot_2]['ties'] += 1
            battle_matrix[bot_2][bot_1]['ties'] += 1

    for trainer in trainer_stats:
        wins = trainer_stats[trainer]['wins']
        losses = trainer_stats[trainer]['losses']
        trainer_stats[trainer]['win_loss_ratio'] = wins / losses if losses != 0 else float('inf')

    sorted_trainer_stats = sorted(trainer_stats.items(), key=lambda item: item[1]['wins'], reverse=True)
    return sorted_trainer_stats, battle_matrix

def calculate_overall_wins(battle_matrix):
    overall_wins = {}
    for trainer1 in battle_matrix:
        overall_wins[trainer1] = sum(record['wins'] for trainer2, record in battle_matrix[trainer1].items() if trainer1 != trainer2)
    return overall_wins

def plot_battle_matrix(battle_matrix):
    # Calculate overall wins for each trainer
    overall_wins = {}
    for trainer1 in battle_matrix:
        overall_wins[trainer1] = sum(record['wins'] for trainer2, record in battle_matrix[trainer1].items() if trainer1 != trainer2)

    # Sort trainers by overall wins in descending order
    sorted_trainers = sorted(overall_wins.keys(), key=lambda t: overall_wins[t], reverse=True)

    # Prepare matrix data with an additional column for the new purple square
    matrix_data = []
    max_wins = 0  # Track maximum number of wins for color scaling
    for trainer1 in sorted_trainers:
        row = []
        for trainer2 in sorted_trainers[::-1]:  # Reverse order for x-axis
            if trainer1 == trainer2:
                row.append(np.nan)  # NaN for battles against themselves
            else:
                record = battle_matrix[trainer1][trainer2]
                wins = record['wins']
                row.append(wins)
                if wins > max_wins:
                    max_wins = wins  # Update max wins
        row.append(overall_wins[trainer1])  # Add overall wins at the end of each row
        row.append(np.nan)  # Add a blank column for the new purple square
        matrix_data.append(row)

    # Convert to numpy array for plotting
    matrix_data = np.array(matrix_data)

    # Create a custom colormap for the main matrix (dark red to green)
    main_cmap = LinearSegmentedColormap.from_list("main_cmap", ["darkred", "green"], N=max_wins+1)

    # Create the plot with a specified figure size
    fig, ax = plt.subplots(figsize=(2500, 2500))

    for i in range(len(sorted_trainers)):
        for j in range(len(sorted_trainers) + 2):  # Include the new purple square column
            val = matrix_data[len(sorted_trainers) - 1 - i, j]  # y-axis in reverse order
            if j == len(sorted_trainers) + 1:  # New blank purple square column
                color = 'purple'
            elif j == len(sorted_trainers):  # Overall column
                color = 'purple' if not np.isnan(val) else 'white'
            else:  # Main matrix
                color = main_cmap(val/max_wins) if not np.isnan(val) else 'white'
            ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, color=color, edgecolor='black', linewidth=50))
            
            # Place the text for battle results and overall wins
            if not np.isnan(val):
                text_color = 'white'
                fontweight = 'bold' if j >= len(sorted_trainers) else 'normal'
                text_val = f"{int(val)}" if j != len(sorted_trainers) + 1 else ''
                text_x = j if j != len(sorted_trainers) else j + 0.5  # Shift text for overall wins
                ax.text(text_x, i, text_val, ha='center', va='center', color=text_color, fontweight=fontweight, fontsize=400)

    # Set axis labels for trainers and blank for the new column
    ax.set_xticks(np.arange(len(sorted_trainers) + 2))
    ax.set_xticklabels(sorted_trainers[::-1] + ['', ''], rotation=90, fontsize=700)  # Remove default 'Overall' label
    ax.set_yticks(np.arange(len(sorted_trainers)))
    ax.set_yticklabels(sorted_trainers[::-1], fontsize=700)

    # Manually place the 'Overall' label at the desired position
    # Adjust the y-coordinate to move the label down by the height of one box
    ax.text(len(sorted_trainers) + 0.5, -2, 'Overall', ha='center', va='center', rotation=90, fontsize=700)

    ax.set_xlim(-0.5, len(sorted_trainers) + 1.5)
    ax.set_ylim(-0.5, len(sorted_trainers) - 0.5)

    # Set titles
    ax.set_title("Ultimate Pokemon Trainer Rankings", fontsize=4000, fontweight='bold', pad=20)
    ax.set_title("100 battles per matchup", fontsize=1600, pad=10, loc='right')

    # Display the plot
    plt.savefig("battle_matrix_plot.png", dpi=10)
    plt.close(fig)

# Use the function and print the results
file_path = 'output.txt'
result, matrix = parse_battles(file_path)
for trainer, record in result:
    print(f"{trainer}: {record['wins']} Wins, {record['losses']} Losses, {record['ties']} Ties, Win/Loss Ratio: {record['win_loss_ratio']:.2f}")

print_battle_matrix(matrix)
plot_battle_matrix(matrix)
