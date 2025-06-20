from PIL import Image
from apng import APNG
import io

# File path for the uploaded APNG
input_apng_path = '/home/gonzalez/Pokemon-Simulator/Data/youtube/Trainer_Sprites/Spr_B2W2_Candice.apng'

# Correct output file path
output_apng_path = '/home/gonzalez/Pokemon-Simulator/Data/youtube/Trainer_Sprites/Spr_B2W2_Candice.apng'

# Open the original APNG file
apng = APNG.open(input_apng_path)

# Initialize an empty list to hold the cropped frames
cropped_frames = []

# Define the crop area (left, upper, right, lower) - you can adjust these values
crop_box = (0, 0, 80, 80)  # Example values, adjust as needed

# Loop through each frame in the APNG
# Calculate crop width and height based on the crop box
crop_width = crop_box[2] - crop_box[0]
crop_height = crop_box[3] - crop_box[1]

# Loop through each frame in the APNG
for frame in apng.frames:
    img, _ = frame  # Unpack the frame tuple (image, delay)

    # Save the PNG image data to a BytesIO buffer so we can open it with Pillow
    img_bytes_io = io.BytesIO(img.to_bytes())  # Use the correct to_bytes method
    
    # Open the image with Pillow
    img_pil = Image.open(img_bytes_io)

    # Resize the image to match the target crop size to avoid shifting
    img_resized = img_pil.resize((crop_width, crop_height), Image.Resampling.LANCZOS)

    # Crop the image (ensure we are centered)
    img_cropped = img_resized.crop(crop_box)
    
    # Append the cropped frame to the list as a temporary file
    temp_file = io.BytesIO()
    img_cropped.save(temp_file, format='PNG')
    temp_file.seek(0)
    cropped_frames.append(temp_file)

# Create a new APNG object
output_apng = APNG()

# Append each cropped frame using the append_file method
for frame in cropped_frames:
    output_apng.append_file(frame)

# Save the cropped APNG
output_apng.save(output_apng_path)

print(f"✅ Cropped APNG saved as {output_apng_path}")

