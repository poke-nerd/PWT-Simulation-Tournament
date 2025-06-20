import json

def generate_brock_vs_brock(input_file, output_file):
    RUN_N_TIMES = 1  # Change to more if you want repeat simulations

    with open(input_file, 'r') as file:
        gym_leaders_data = json.load(file)

    # Safely get Brock's team
    brock_team = gym_leaders_data["Alder"]

    # Generate one or more Brock vs Brock matchups
    matchups = [[brock_team, brock_team] for _ in range(RUN_N_TIMES)]

    with open(output_file, 'w') as file:
        json.dump(matchups, file, indent=2)

# Run it
generate_brock_vs_brock("Inputs/GymLeaderTeams.json", "Inputs/tournament_battles.json")
