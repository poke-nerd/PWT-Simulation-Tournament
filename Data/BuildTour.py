import json

def generate_full_tournament(input_file, output_file, runs_per_matchup=1):
    with open(input_file, 'r') as f:
        gym_leader_teams = json.load(f)

    trainer_names = list(gym_leader_teams.keys())
    matchups = []

    # Every trainer battles every other trainer (excluding self), repeated N times
    for i in range(len(trainer_names)):
        for j in range(i + 1, len(trainer_names)):
            team1 = gym_leader_teams[trainer_names[i]]
            team2 = gym_leader_teams[trainer_names[j]]
            for _ in range(runs_per_matchup):
                matchups.append([team1, team2])

    with open(output_file, 'w') as f:
        json.dump(matchups, f, indent=2)

    print(f"Saved {len(matchups)} battles to {output_file} (each matchup repeated {runs_per_matchup} times)")

if __name__ == "__main__":
    input_file = "Inputs/GymLeaderTeams.json"
    output_file = "Inputs/tournament_battles.json"
    generate_full_tournament(input_file, output_file, runs_per_matchup=1)

