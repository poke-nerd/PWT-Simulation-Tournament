import json
import os
from PIL import Image, ImageDraw, ImageFont

# Load the trainer data (assuming the uploaded file is 'index.json')
with open('index.json', 'r') as f:
    trainer_data = json.load(f)

# Directory where trainer card image files are stored
output_dir = './Output/'

# Function to find and process trainer cards (now looking for image files)
def get_trainer_card(trainer_name, output_dir):
    # List all files in the Output directory
    files = os.listdir(output_dir)
    
    # Search for the trainer card image file by matching the format 'trainer_name_card.png'
    for filename in files:
        if filename.startswith(trainer_name) and filename.endswith('_card.png'):
            return os.path.join(output_dir, filename)
    
    return None

# Function to add Pokémon names in a 2x3 grid layout
def add_pokemon_names_to_card(card_path, pokemon_names):
    # Open the image
    with Image.open(card_path) as img:
        draw = ImageDraw.Draw(img)

        # Font and size for the text
        try:
            font = ImageFont.truetype("arial.ttf", 40)  # Change the font size as needed
        except IOError:
            font = ImageFont.load_default()  # Fallback if custom font is not available

        # Coordinates for 2 rows and 3 columns layout
        width, height = img.size
        padding = 10  # Space between text blocks
        x_offset = 50  # Start x position
        y_offset = 100  # Start y position

        # Loop to place Pokémon names in the grid
        for i, pokemon_name in enumerate(pokemon_names):
            row = i // 3  # Determine row (0 or 1)
            col = i % 3   # Determine column (0, 1, or 2)

            # Calculate x and y position
            x = x_offset + col * (width // 3)  # Evenly distribute across the width
            y = y_offset + row * (height // 2)  # Evenly distribute across the height

            # Add Pokémon name to the image at the calculated position
            draw.text((x, y), pokemon_name, fill="white", font=font)

        # Save the image back with the same filename (overwriting the original)
        img.save(card_path)  # Overwrites the original file
        print(f"Modified card saved: {card_path}")

# Loop through trainer data
for trainer in trainer_data:
    trainer_name = trainer[0]  # Extract the trainer's name from the JSON
    pokemon_name = trainer[1]  # Extract the Pokémon's name
    print(f"Looking for trainer: {trainer_name} with Pokémon: {pokemon_name}")
    
    # Get the corresponding trainer card from the files in the Output directory
    card_path = get_trainer_card(trainer_name, output_dir)
    
    if card_path:
        print(f"Found card for {trainer_name}: {card_path}")
        
        # Get all Pokémon names for the trainer (in case there are multiple Pokémon)
        trainer_pokemon_names = [entry[1] for entry in trainer_data if entry[0] == trainer_name]
        
        # Add the Pokémon names in a 2x3 grid layout
        add_pokemon_names_to_card(card_path, trainer_pokemon_names)
    else:
        print(f"No card found for {trainer_name}")

