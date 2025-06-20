import os
import re

def split_file_by_trainer_names(input_path, output_dir="battles_html"):
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    in_block = False
    block_lines = []
    trainer_line = ""
    count = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("[[[[["):
            in_block = True
            block_lines = [line]
            trainer_line = ""  # reset for new block

        elif in_block and not trainer_line and " vs " in stripped:
            trainer_line = stripped
            block_lines.append(line)

        elif stripped.startswith("]]]]]") and in_block:
            block_lines.append(line)
            in_block = False
            count += 1

            # clean filename from trainer names
            if " vs " in trainer_line:
                t1, t2 = trainer_line.split(" vs ")
                filename = f"{t1.strip()}_vs_{t2.strip()}.txt"
                filename = re.sub(r'[^\w\-_\. ]', '_', filename)  # sanitize filename
            else:
                filename = f"battle_{count}.txt"

            output_file = os.path.join(output_dir, filename)
            with open(output_file, "w", encoding="utf-8") as out:
                out.writelines(block_lines)

        elif in_block:
            block_lines.append(line)

    print(f"✅ Extracted {count} battles to '{output_dir}/'")

if __name__ == "__main__":
    # Change this to your specific Tour100 file
    input_file = "Tour100/output100.txt"
    split_file_by_trainer_names(input_file)

