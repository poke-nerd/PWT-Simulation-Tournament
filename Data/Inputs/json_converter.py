import json

def generate_gym_leader_teams(pokemon_file, trainer_file, output_file):
    # Read trainer names (stripping numbering prefix like 01_)
    with open(trainer_file, 'r', encoding='utf-8') as f:
        trainer_names = [line.strip().split("_", 1)[1] for line in f if line.strip()]

    # Read GymLeaderPokemon.txt contents
    with open(pokemon_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]

    trainer_teams = {}
    lines_per_pokemon = 9  # Pokémon, Ability, EVs, Level, 4 Moves, blank line
    pokemon_per_trainer = 6
    lines_per_trainer = lines_per_pokemon * pokemon_per_trainer

    for i, trainer in enumerate(trainer_names):
        start_line = i * lines_per_trainer
        team = []
        for j in range(pokemon_per_trainer):
            pokemon_line = lines[start_line + j * lines_per_pokemon].strip()
            pokemon_name = pokemon_line.split("@")[0].strip().lstrip("|").strip()
            line_number = start_line + j * lines_per_pokemon + 1  # 1-indexed
            team.append([pokemon_name, line_number])
        trainer_teams[trainer] = team

    # Save JSON output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(trainer_teams, f, indent=4)

if __name__ == "__main__":
    generate_gym_leader_teams(
        pokemon_file="GymLeaderPokemon.txt",
        trainer_file="trainers.txt",
        output_file="GymLeaderTeams.json"
    )

