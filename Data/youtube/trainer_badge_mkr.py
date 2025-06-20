import os
import json
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
from apng import APNG
import tempfile
import re
# === Helper to load .apng frames using PIL and remove embedded blue background safely ===
def load_apng_frames(path):
    try:
        if not path.endswith(".apng"):
            return None
        img = Image.open(path)
        frames = []

        for frame in range(0, img.n_frames):
            img.seek(frame)
            frame_copy = img.copy().convert("RGBA")
            np_img = np.array(frame_copy)

            # Zero out low alpha pixels, ensuring transparency is fully cleaned
            r, g, b, a = np_img[..., 0], np_img[..., 1], np_img[..., 2], np_img[..., 3]
            low_alpha_mask = a < 30  # Adjust alpha threshold as needed
            np_img[low_alpha_mask] = [0, 0, 0, 0]  # Remove color

            # Ensure no blue color is left behind in transparent areas
            blue_mask = (r < 100) & (g < 100) & (b > 180) & (a > 0)
            np_img[blue_mask] = [0, 0, 0, 0]  # Remove any lingering blue edges

            cleaned = Image.fromarray(np_img, mode="RGBA")
            frames.append(cleaned)

        return frames
    except Exception as e:
        print(f"⚠️ Failed to load APNG: {path}, Error: {e}")
        return None

# === Save APNG using apng module ===
def save_apng(frames, output_path, duration):
    with tempfile.TemporaryDirectory() as tmpdir:
        part_paths = []
        for i, frame in enumerate(frames):
            path = os.path.join(tmpdir, f"frame_{i}.png")
            frame.save(path)
            part_paths.append(path)  # Ensure this is properly aligned
        apng = APNG()
        for path in part_paths:
            apng.append_file(path, delay=int(duration))
        apng.save(output_path)

# === Paths ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "Templates", "card_template.png")
TRAINER_SPRITES = os.path.join(SCRIPT_DIR, "Trainer_Sprites")
POKEMON_SPRITES = os.path.join(SCRIPT_DIR, "Pokemon_Sprites")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Output")
DATA_PATH = os.path.join(SCRIPT_DIR, "data.json")
POKEMON_TXT_PATH = os.path.join(SCRIPT_DIR, "GymLeaderPokemon.txt")
item_icon_path = os.path.join(SCRIPT_DIR, "Item")
MASTER_STATS_PATH = os.path.join(SCRIPT_DIR, "..", "master_trainer_stats.csv")

stats_df = pd.read_csv(MASTER_STATS_PATH)
stats_df['Trainer'] = stats_df['Trainer'].str.lower()
trainer_stats = stats_df.set_index("Trainer").to_dict(orient="index")

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 24
SMALL_FONT_SIZE = 12
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
small_font = ImageFont.truetype(FONT_PATH, SMALL_FONT_SIZE)

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(DATA_PATH, "r") as f:
    trainer_data = json.load(f)

with open(POKEMON_TXT_PATH, "r", encoding="utf-8") as f:
    pokemon_txt_lines = [line.strip() for line in f.readlines()]

def get_pokemon_block(index):
    start = index - 1
    block = pokemon_txt_lines[start:start + 8]
    cleaned = block[:2] + block[4:]

    if cleaned:
        parts = cleaned[0].split("@")
        name = parts[0].strip()
        item = parts[1].strip() if len(parts) > 1 else "None"
        cleaned[0] = name

    if cleaned:
        parts = cleaned[1].split(":")
        name = parts[1].strip()
        a_name = parts[2].strip() if len(parts) > 2 else "None"
        cleaned[1] = name
        cleaned.insert(1, f"Ability:")
    if cleaned:
        cleaned[0] = cleaned[0][1:]
    return cleaned

def get_held_item_name(index):
    start = index - 1
    block = pokemon_txt_lines[start:start + 1]
    if not block:
        return None
    first_line = block[0]
    parts = first_line.split("@")
    if len(parts) > 1:
        return parts[1].strip()
    return None

def generate_trainer_card(trainer_name, pokemon_list):
    base_card = Image.open(TEMPLATE_PATH).convert("RGBA") if os.path.exists(TEMPLATE_PATH) else Image.new("RGBA", (600, 400), (255, 255, 255, 0))

    trainer_sprite_path = os.path.join(TRAINER_SPRITES, f"Spr_B2W2_{trainer_name}.apng")
    trainer_frames = load_apng_frames(trainer_sprite_path)
    if not trainer_frames:
        print(f"⚠️ Missing trainer APNG: {trainer_sprite_path}")
        return

    poke_frame_lists, info_blocks, held_items = [], [], []
    for poke_name, index in pokemon_list:
        sprite_path = os.path.join(POKEMON_SPRITES, f"{poke_name}.apng")
        frames = load_apng_frames(sprite_path)
        poke_frame_lists.append(frames if frames else [])
        info_blocks.append(get_pokemon_block(index))
        held_items.append(get_held_item_name(index))

    max_frame_count = max([len(frames) for frames in poke_frame_lists if frames] + [len(trainer_frames)])
    duration = 75
    output_frames = []

    for frame_idx in range(max_frame_count):
        frame_to_use = min(frame_idx, len(trainer_frames)-1)
        card = base_card.copy()
        draw = ImageDraw.Draw(card, "RGBA")

        # Box dimensions for the trainer sprite
        box_w, box_h = 120, 120
        base_x, base_y = 40, 75

        trainer_img = trainer_frames[frame_to_use].resize((100, 100), resample=Image.Resampling.LANCZOS)

        # Calculate the offsets to center the image in the box
        offset_x = base_x + (box_w - 100) // 2
        offset_y = base_y + (box_h - 100) // 2

        # Draw the box around the trainer sprite
        draw.rounded_rectangle([base_x, base_y, base_x + box_w, base_y + box_h], radius=12, fill=(200, 200, 200, 255), outline="black", width=2)

        # Paste the trainer sprite inside the box
        card.alpha_composite(trainer_img, (offset_x, offset_y))

        name_box_x, name_box_y, name_box_w, name_box_h = 5, 20, 200, 40
        draw.rectangle([name_box_x, name_box_y, name_box_x + name_box_w, name_box_y + name_box_h], fill=(200, 200, 200, 255), outline="black", width=2)
        bbox = draw.textbbox((0, 0), trainer_name, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((name_box_x + (name_box_w - text_w) // 2, name_box_y + 8), trainer_name, font=font, fill="black")

        stats = trainer_stats.get(trainer_name.lower(), {})
        


        # Retrieve the toughest and easiest opponents as lists
        trainers_w = stats.get("toughest_opponent", ["N/A"])  # Default to ["N/A"] if no matchups
        trainers_l = stats.get("easiest_opponent", ["N/A"])    # Default to ["N/A"] if no matchups

        # Debugging: print the values of trainers_w and trainers_l
        #print(f"Debug: Toughest Opponents for {trainer}: {trainers_w}")
        #print(f"Debug: Easiest Opponents for {trainer}: {trainers_l}")

        # Check if the data is in list format and join it into a comma-separated string
        if isinstance(trainers_w, list) and trainers_w != ["N/A"]:
            toughest_matchups = ", ".join(trainers_w)
        else:
            toughest_matchups = "N/A"  # If there are no matchups or it's an empty list

        if isinstance(trainers_l, list) and trainers_l != ["N/A"]:
            easiest_matchups = ", ".join(trainers_l)
        else:
            easiest_matchups = "N/A"  # If there are no matchups or it's an empty list

        # Retrieve other trainer stats
        placement = stats.get("Placement", "N/A")
        tier = stats.get("Tier", "N/A")
        elo = stats.get("Elo", "N/A")
        raw_ratio = stats.get("win_loss_ratio", "N/A")
        wl_ratio = f"{float(raw_ratio):.3f}" if isinstance(raw_ratio, (float, int)) else raw_ratio

        trainers_w = re.sub(r"[\[\]']", '', trainers_w)  # removes [, ], and '
        trainers_w = ', '.join([name.strip() for name in trainers_w.split(',')])

        trainers_l = re.sub(r"[\[\]']", '', trainers_l)  # removes [, ], and '
        trainers_l = ', '.join([name.strip() for name in trainers_l.split(',')])


        # Create the stats lines, including the correctly formatted toughest and easiest matchups
        stats_lines = [
            f"Placement: {placement}",
            f"Tier: {tier}",
            f"Elo: {elo}",
            f"W/L: {wl_ratio}",
            f"Toughest Matchup:", 
            f"{trainers_w}",
            f"Easiest Matchup:",
            f"{trainers_l}"
        ]

        # Debugging: print the final stats_lines to check the output
        #print(f"Debug: Final stats for {trainer}: {stats_lines}")








        stats_box_x, stats_box_y = 25, 235
        box_right = stats_box_x + 145
        box_bottom = stats_box_y + len(stats_lines) * 15 + 5
        draw.rectangle([stats_box_x - 20, stats_box_y - 5, box_right, box_bottom], fill=(200, 200, 200, 255), outline="black", width=2)
        for i, line in enumerate(stats_lines):
            draw.text((stats_box_x-10, stats_box_y + i * 15), line, font=small_font, fill="black")

        for i, frames in enumerate(poke_frame_lists):
            if not frames:
                continue
            poke_idx = frame_idx % len(frames) 
            poke_img = frames[poke_idx].resize((60, 60), resample=Image.Resampling.LANCZOS)
            col, row = i % 3, i // 3
            box_x, box_y = 220 + col * 135, 15 + row * 195
            draw.rounded_rectangle([box_x - 6, box_y - 6, box_x + 66, box_y + 66], radius=12, fill=(200, 200, 200, 255), outline="black", width=2)
            card.paste(poke_img, (box_x, box_y), poke_img)

            if info_blocks[i]:
                text_lines = [line.strip() for line in info_blocks[i]]
                text_y = box_y + 75
                text_x = box_x - 10
                text_padding = 10
                overlay = Image.new("RGBA", card.size, (255, 255, 255, 0))
                overlay_draw = ImageDraw.Draw(overlay, "RGBA")
                overlay_draw.rectangle(
                    [text_x - text_padding - 5,
                     text_y - text_padding + 5,
                     text_x + 95 + text_padding,
                     text_y + len(text_lines) * 15 + text_padding - 5],
                    fill=(255, 255, 255, 180),
                    outline="black",
                    width=4
                )
                card.alpha_composite(overlay)
                for line in text_lines:
                    draw.text((text_x - 5, text_y), line, font=small_font, fill="black")
                    text_y += 15

            held_item_name = held_items[i]
            if held_item_name:
                item_file = "Bag_" + held_item_name.replace(" ", "_") + "_Sprite.png"
                icon_path = os.path.join(item_icon_path, item_file)
                if os.path.exists(icon_path):
                    item_img = Image.open(icon_path).convert("RGBA").resize((30, 30), resample=Image.Resampling.LANCZOS)
                    card.paste(item_img, (box_x + 30, box_y + 30), item_img)

        output_frames.append(card.copy())  # ensure clean reference per frame

    output_base = os.path.join(OUTPUT_DIR, f"{trainer_name}_card")
    save_apng(output_frames, output_base + ".apng", duration)
    print(f"✅ Saved animated card: {output_base}.apng")

    png_frame = output_frames[-1].convert("RGBA")
    png_frame.save(output_base + ".png", format="PNG")
    print(f"✅ Saved static card (PNG): {output_base}.png")

    gif_frames = [frame.convert("RGBA") for frame in output_frames]
    gif_frames[0].save(
        output_base + ".gif",
        save_all=True,
        append_images=gif_frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        optimize=False
    )
    print(f"✅ Saved animated card (GIF): {output_base}.gif")

for trainer, team in trainer_data.items():
    generate_trainer_card(trainer, team)

