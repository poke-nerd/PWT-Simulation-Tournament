import os
import re
from collections import defaultdict

def count_trainer_battles(file_path):
    trainer_battle_counts = defaultdict(int)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split by battle delimiters
    battles = re.split(r'\[\[\[\[\[|\]\]\]\]\]', content)[1:-1]
    name_pattern = re.compile(r'^(.*?) vs (.*?)\n', re.MULTILINE)

    for battle in battles:
        match = name_pattern.search(battle)
        if not match:
            continue
        bot_1, bot_2 = match.groups()
        trainer_battle_counts[bot_1] += 1
        trainer_battle_counts[bot_2] += 1

    return trainer_battle_counts

def main():
    output_folder = "Tour100"
    all_trainers = set()
    missing_report = {}

    for filename in sorted(os.listdir(output_folder)):
        if filename.startswith("output") and filename.endswith(".txt"):
            file_path = os.path.join(output_folder, filename)
            trainer_counts = count_trainer_battles(file_path)

            # Update global trainer list
            all_trainers.update(trainer_counts.keys())

            # Check for trainers with < 72 battles
            missing = {t: c for t, c in trainer_counts.items() if c < 72}

            if missing:
                print(f"\n{filename} - Trainers with < 72 battles:")
                for trainer, count in sorted(missing.items(), key=lambda x: x[0]):
                    print(f"  {trainer}: {count} battles")
                missing_report[filename] = missing

    print("\n✅ Check complete.")
    if not missing_report:
        print("All trainers had at least 72 battles in each file.")
    else:
        print(f"{len(missing_report)} files had missing battles. See above.")

if __name__ == "__main__":
    main()

