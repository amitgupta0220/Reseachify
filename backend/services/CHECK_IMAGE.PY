import base64
from io import BytesIO
from PIL import Image
import json
import os

# Load the base64 data from the JSON file
with open("images.json", "r") as file:
    base64_images = json.load(file)

# Decode and save each image
output_dir = "./decoded_images"
os.makedirs(output_dir, exist_ok=True)

for i, image_base64 in enumerate(base64_images):
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))
    image.save(f"{output_dir}/image_{i+1}.png")

print(f"Images have been saved to {output_dir}")
