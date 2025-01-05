from PIL import Image
import os
import shutil

# Directory containing JPG images
INPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/random" 
OUTPUT_PATH = os.path.join(INPUT_PATH, "edge_problem")            

def has_white_pixels_at_edges(image_path):
    """
    Check if an image has white pixels at its edges.
    """
    with Image.open(image_path) as img:
        # Convert to grayscale for simplicity
        img = img.convert("L")
        img_data = img.load()

        width, height = img.size

        # Check top and bottom edges
        for x in range(width):
            if img_data[x, 0] == 255 or img_data[x, height - 1] == 255:
                return True

        # Check left and right edges
        for y in range(height):
            if img_data[0, y] == 255 or img_data[width - 1, y] == 255:
                return True

    return False

def move_images_with_white_edges(image_dir, bad_dir):
    """
    Move images with white pixels at the edges to the 'bad' subdirectory.
    """
    if not os.path.exists(bad_dir):
        os.makedirs(bad_dir)

    for file_name in os.listdir(image_dir):
        if file_name.lower().endswith(".jpg"):
            image_path = os.path.join(image_dir, file_name)
            if has_white_pixels_at_edges(image_path):
                # Move the file to the 'bad' subdirectory
                shutil.move(image_path, os.path.join(bad_dir, file_name))
                print(f"Moved to bad: {file_name}")

# Run the scan and move bad images
move_images_with_white_edges(INPUT_PATH, OUTPUT_PATH)

print("Processing complete.")
