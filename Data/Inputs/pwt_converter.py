# generate_gym_leader_pokemon.py

def read_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def generate_gym_leader_pokemon(pokemon_file, items_file, moves_file, abilities_file, output_file):
    pokemon = read_txt_file(pokemon_file)
    items = read_txt_file(items_file)
    moves = read_txt_file(moves_file)
    abilities = read_txt_file(abilities_file)

    num_trainers = 73
    team_size = 6
    moves_per_pokemon = 4

    output = ''
    for i in range(num_trainers):
        for j in range(team_size):
            poke_index = i * team_size + j
            output += f"| {pokemon[poke_index]} @ {items[poke_index]}\n"
            output += f"{abilities[poke_index]}\n"
            output += "EVs: 1 HP\n"
            output += "Level: 50\n"
            for k in range(moves_per_pokemon):
                move_index = poke_index * moves_per_pokemon + k
                output += f"- {moves[move_index]}\n"
            output += '\n'

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(output)

if __name__ == "__main__":
    generate_gym_leader_pokemon(
        pokemon_file="pokemon.txt",
        items_file="items.txt",
        moves_file="moves.txt",
        abilities_file="ordered_abilities.txt",
        output_file="GymLeaderPokemon.txt"
    )

