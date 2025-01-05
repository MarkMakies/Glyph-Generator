from PIL import Image
import os
from random import randint as RI

# Constants
GRID_SIZE = 16  # Number of cells/blocks
PIXEL_SIZE = 8  # Size of each pixel in output images

MIN_COLOUR_LEVEL = 128
MAX_COLOUR_LEVEL = 256

INPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/glyphs_random/" 
OUTPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/glyphs_random/coloured" 

# Ensure the output directory exists
os.makedirs(OUTPUT_PATH, exist_ok=True)

def colourize_glyph(input_file, output_file):
    """Reads a glyph image, colorizes white cells, and saves the result."""
    # Open the image
    img = Image.open(input_file)
    img = img.convert("RGB")  # Ensure the image is in RGB format

    # Convert the image to a 16x16 matrix
    matrix = [[(0, 0, 0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Check the top-left pixel of each cell (block) to determine if it's white
            x = col * PIXEL_SIZE
            y = row * PIXEL_SIZE
            pixel = img.getpixel((x, y))
            if pixel == (255, 255, 255):  # If the cell is white
                # Generate a random color
                new_colour = (
                    RI(MIN_COLOUR_LEVEL, MAX_COLOUR_LEVEL), 
                    RI(MIN_COLOUR_LEVEL, MAX_COLOUR_LEVEL), 
                    RI(MIN_COLOUR_LEVEL, MAX_COLOUR_LEVEL)
                )
                matrix[row][col] = new_colour

    # Create a new image and fill it with the colorized matrix
    new_img = Image.new("RGB", img.size, "black")
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = matrix[row][col]
            # Draw the colorized block
            for x in range(PIXEL_SIZE):
                for y in range(PIXEL_SIZE):
                    new_img.putpixel((col * PIXEL_SIZE + x, row * PIXEL_SIZE + y), color)

    # Save the new image
    new_img.save(output_file)
    print(f"Processed and saved: {output_file}")

def colourize_glyphs_in_directory(input_path, output_path):
    """Processes all glyphs in the input directory and saves the colorized versions."""
    for file_name in os.listdir(input_path):
        input_file = os.path.join(input_path, file_name)
        output_file = os.path.join(output_path, file_name)
        if os.path.isfile(input_file) and file_name.endswith(".jpg"):  # Process only JPG files
            colourize_glyph(input_file, output_file)

# Run the colorization process
colourize_glyphs_in_directory(INPUT_PATH, OUTPUT_PATH)
