from PIL import Image
import os

# Parameters
INPUT_PATH = "/home/mark/Projects/Glyph Generator/data/test/"
OUTPUT_PATH = "/home/mark/Projects/Glyph Generator/data/test_rotated/"

# Ensure output directory exists
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

def rotate_and_save_images():
    """Processes images by rotating them 90, 180, and 270 degrees and saving copies."""
    image_files = [f for f in os.listdir(INPUT_PATH) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    for image_file in image_files:
        input_file_path = os.path.join(INPUT_PATH, image_file)
        
        try:
            # Open the image
            with Image.open(input_file_path) as img:
                
                # Extract base name without extension
                base_name, ext = os.path.splitext(image_file)

                # Rotate and save 90 degrees
                rotated_90 = img.rotate(90, expand=True)
                rotated_90.save(os.path.join(OUTPUT_PATH, f"{base_name}R90{ext}"))

                # Rotate and save 180 degrees
                rotated_180 = img.rotate(180, expand=True)
                rotated_180.save(os.path.join(OUTPUT_PATH, f"{base_name}R180{ext}"))

                # Rotate and save 270 degrees
                rotated_270 = img.rotate(270, expand=True)
                rotated_270.save(os.path.join(OUTPUT_PATH, f"{base_name}R270{ext}"))

                print(f"Processed {image_file} -> Rotated copies saved.")
        except Exception as e:
            print(f"Failed to process {image_file}: {e}")

# Run the rotation script
rotate_and_save_images()
