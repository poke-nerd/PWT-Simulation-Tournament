import os
import subprocess
import time

# Make sure Tour100 exists
os.makedirs("Tour100", exist_ok=True)

EXPECTED_BATTLES = 72 #(73 * 72) // 2  # 2628
MAX_ITERATIONS = 100

def get_latest_output_number(base_dir="Tour100", base_name="output", extension=".txt"):
    i = 1
    while os.path.exists(os.path.join(base_dir, f"{base_name}{i}{extension}")):
        i += 1
    return i - 1

def is_output_valid(path, min_battles):
    if not os.path.exists(path):
        return False
    with open(path, 'r', encoding="utf-8") as f:
        content = f.read()
    return content.count("]]]]]\n") >= min_battles

def run_simulation_script(output_path):
    print(f"🔁 Running tournament iteration: {output_path}")
    subprocess.run(["python3", "runSimulations.py", output_path])

def main_loop():
    base_dir = "Tour100"
    base_name = "output"
    extension = ".txt"

    current_iteration = 0  # Start from output81.txt
    while current_iteration < MAX_ITERATIONS:
        next_output_file = os.path.join(base_dir, f"{base_name}{current_iteration + 1}{extension}")

        if not is_output_valid(next_output_file, EXPECTED_BATTLES):
            print(f"⛔ {next_output_file} missing or incomplete (< {EXPECTED_BATTLES} battles). Retrying simulation...")
            run_simulation_script(next_output_file)
            time.sleep(2)
        else:
            print(f"✅ {next_output_file} complete. Proceeding to next iteration.")
            current_iteration += 1

    print(f"🎉 All {MAX_ITERATIONS} iterations complete. Wrapper exiting.")

if __name__ == "__main__":
    main_loop()

