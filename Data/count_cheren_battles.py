import os
import re
from collections import defaultdict

def count_cheren_battles(file_path):
    cheren_battles = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content by battle delimiters (assuming standard format)
    battles = re.split(r'\[\[\[\[\[|\]\]\]\]\]', content)[1:-1]
    name_pattern = re.compile(r'^(.*?) vs (.*?)\n', re.MULTILINE)

    # Count how many times Cheren battles
    for battle in battles:
        match = name_pattern.search(battle)
        if match:
            bot_1, bot_2 = match.groups()
            if "Morty" in bot_1 or "Morty" in bot_2:
                cheren_battles += 1

    return cheren_battles

def main():
    output_folder = "Tour100"  # Change this to your folder path if different
    total_cheren_battles = 0

    # Loop through the files in the output folder
    for filename in sorted(os.listdir(output_folder)):
        if filename.startswith("output") and filename.endswith(".txt"):
            file_path = os.path.join(output_folder, filename)

            # Count battles involving Cheren in this file
            cheren_battles = count_cheren_battles(file_path)
            print(f"{filename}: Cheren participated in {cheren_battles} battles.")
            total_cheren_battles += cheren_battles

    print(f"\nTotal Cheren battles across all files: {total_cheren_battles}")

if __name__ == "__main__":
    main()

