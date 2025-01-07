from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import os
import math
import random

# Paths
INPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/glyphs"
OUTPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/sheets_test"

# Glyph and Mosaic Configuration
GLYPH_CANVAS_SIZE = (512, 512)  # Size for each glyph's canvas, original glyphs 128x128
MOSAIC_ROWS = 23  # Number of rows in the mosaic
MOSAIC_COLS = 30  # Number of columns in the mosaic
MOSAIC_PADDING = 128  # Padding between glyphs and edges of the mosaic (in pixels)
GLYPH_HORIZ_PADDING = -96  # Horizontal spacing between glyphs
GLYPH_VERT_PADDING = -96  # Vertical spacing between glyphs
EDGE_COLOUR = (0, 0, 0)  # Edge padding color (default is black)
FINAL_DOWNSCALE = 0.75  # Scale factor for downscaling the final output (e.g., 0.5 for half-size)

# Rotation probabilities (in percent)
PROB_ROTATION_0 = 60
PROB_ROTATION_90 = 20
PROB_ROTATION_180 = 10
PROB_ROTATION_270 = 10

# Automatically calculate MOSAIC_SIZE
MOSAIC_SIZE = (
    MOSAIC_PADDING * 2 + MOSAIC_COLS * (GLYPH_CANVAS_SIZE[0] + GLYPH_HORIZ_PADDING) - GLYPH_HORIZ_PADDING,
    MOSAIC_PADDING * 2 + MOSAIC_ROWS * (GLYPH_CANVAS_SIZE[1] + GLYPH_VERT_PADDING) - GLYPH_VERT_PADDING,
)

def difference_of_gaussians(image, radius1, radius2, threshold=30):
    """Applies Difference of Gaussians filter with a threshold."""
    blur1 = image.filter(ImageFilter.GaussianBlur(radius1))
    blur2 = image.filter(ImageFilter.GaussianBlur(radius2))
    
    arr1 = np.array(blur1, dtype=np.float32)
    arr2 = np.array(blur2, dtype=np.float32)
    dog = arr1 - arr2
    
    # Thresholding to remove noise
    dog[dog < threshold] = 0  # Suppress weak edges
    dog[dog >= threshold] = 255  # Highlight strong edges
    
    return Image.fromarray(dog.astype('uint8'))

def choose_rotation():
    """Chooses a random rotation angle based on probabilities."""
    rand = random.uniform(0, 100)
    if rand < PROB_ROTATION_0:
        return 0
    elif rand < PROB_ROTATION_0 + PROB_ROTATION_90:
        return 90
    elif rand < PROB_ROTATION_0 + PROB_ROTATION_90 + PROB_ROTATION_180:
        return 180
    else:
        return 270

def create_artistic_sheets():
    """Generates artistic proof sheets."""
    glyph_files = [f for f in os.listdir(INPUT_PATH) if f.endswith(".jpg")]
    glyph_count = len(glyph_files)
    glyphs_per_sheet = MOSAIC_ROWS * MOSAIC_COLS

    # Number of sheets needed
    sheet_count = math.ceil(glyph_count / glyphs_per_sheet)

    print(f"Generating {sheet_count} artistic mosaic sheets...")

    for sheet_idx in range(sheet_count):
        # Create a blank mosaic with the edge color
        mosaic = Image.new("RGB", MOSAIC_SIZE, EDGE_COLOUR)

        for i in range(glyphs_per_sheet):
            glyph_idx = sheet_idx * glyphs_per_sheet + i
            if glyph_idx >= glyph_count:
                break

            glyph_path = os.path.join(INPUT_PATH, glyph_files[glyph_idx])
            glyph_img = Image.open(glyph_path).convert("RGB")

            print(f"Processing: {glyph_files[glyph_idx]}")

            # Resize to canvas size
            glyph_img = glyph_img.resize(GLYPH_CANVAS_SIZE, Image.LANCZOS)

            # Apply artistic effects
            glyph_img = glyph_img.filter(ImageFilter.GaussianBlur(13))
            glyph_img = glyph_img.filter(ImageFilter.SMOOTH_MORE)
            glyph_img = ImageEnhance.Contrast(glyph_img).enhance(1.8)
            glyph_img = ImageEnhance.Brightness(glyph_img).enhance(1.2)

            # Apply Difference of Gaussians filter
            glyph_img = difference_of_gaussians(glyph_img, radius1=1, radius2=30)

            # Choose a random rotation angle
            rotation_angle = choose_rotation()
            glyph_img = glyph_img.rotate(rotation_angle, expand=True)

            # Calculate position with padding and spacing
            col = i % MOSAIC_COLS
            row = i // MOSAIC_COLS
            x = MOSAIC_PADDING + col * (GLYPH_CANVAS_SIZE[0] + GLYPH_HORIZ_PADDING)
            y = MOSAIC_PADDING + row * (GLYPH_CANVAS_SIZE[1] + GLYPH_VERT_PADDING)

            # Paste glyph into the mosaic
            mosaic.paste(glyph_img, (x, y))

        # Downscale the mosaic if FINAL_DOWNSCALE is set
        if FINAL_DOWNSCALE != 1.0:
            new_width = int(mosaic.width * FINAL_DOWNSCALE)
            new_height = int(mosaic.height * FINAL_DOWNSCALE)
            mosaic = mosaic.resize((new_width, new_height), Image.LANCZOS)

        # Save the mosaic sheet
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        mosaic_path = os.path.join(OUTPUT_PATH, f"Artistic_Sheet_{sheet_idx + 1}.jpg")
        mosaic.save(mosaic_path, "JPEG")
        print(f"Saved {mosaic_path}")

# Run the artistic proof sheet generator
create_artistic_sheets()
