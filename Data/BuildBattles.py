import json
import random

def generate_random_vs_all(input_file, output_file):
    with open(input_file, 'r') as f:
        gym_leader_teams = json.load(f)

    trainer_names = list(gym_leader_teams.keys())
    anchor_trainer = "Morty"#random.choice(trainer_names)
    anchor_team = gym_leader_teams[anchor_trainer]

    # Exclude self to avoid mirror match (or include it if desired)
    matchups = [[anchor_team, gym_leader_teams[opponent]]
                for opponent in trainer_names if opponent != anchor_trainer]

    with open(output_file, 'w') as f:
        json.dump(matchups, f, indent=2)

    print(f"{anchor_trainer} vs {len(matchups)} other trainers saved to {output_file}")

if __name__ == "__main__":
    input_file = "Inputs/GymLeaderTeams.json"
    output_file = "Inputs/tournament_battles.json"
    generate_random_vs_all(input_file, output_file)

