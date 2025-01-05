from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import os
import math

# Parameters

INPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/random" 
OUTPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/sheets" 

GLYPH_CANVAS_SIZE = (512, 512)  # Size for each glyph's canvas, original glyphs 128x128
MOSAIC_ROWS = 24  # Number of rows in the mosaic
MOSAIC_COLS = 24  # Number of columns in the mosaic
MOSAIC_PADDING = 0  # Padding between glyphs and edges of the mosaic (in pixels)

# Automatically calculate MOSAIC_SIZE
MOSAIC_SIZE = (
    MOSAIC_COLS * GLYPH_CANVAS_SIZE[0] + (MOSAIC_PADDING * 2),
    MOSAIC_ROWS * GLYPH_CANVAS_SIZE[1] + (MOSAIC_PADDING * 2),
)                                     

def difference_of_gaussians(image, radius1, radius2, threshold=30):
    """Applies Difference of Gaussians filter with a threshold."""
    # Apply Gaussian blur with two different radii                                           
    blur1 = image.filter(ImageFilter.GaussianBlur(radius1))
    blur2 = image.filter(ImageFilter.GaussianBlur(radius2))
    
    arr1 = np.array(blur1, dtype=np.float32)
    arr2 = np.array(blur2, dtype=np.float32)
    dog = arr1 - arr2
    
    # Thresholding to remove noise
    dog[dog < threshold] = 0  # Suppress weak edges
    dog[dog >= threshold] = 255  # Highlight strong edges
    
    # Convert back to an image
    dog_image = Image.fromarray(dog.astype('uint8'))
    return dog_image

def create_artistic_sheets():
    """Generates artistic proof sheets."""
    glyph_files = [f for f in os.listdir(INPUT_PATH) if f.endswith(".jpg")]
    glyph_count = len(glyph_files)
    glyphs_per_sheet = MOSAIC_ROWS * MOSAIC_COLS

    # Number of sheets needed
    sheet_count = math.ceil(glyph_count / glyphs_per_sheet)

    print(f"Generating {sheet_count} artistic mosaic sheets...")

    for sheet_idx in range(sheet_count):
        # Create a blank mosaic with padding
        mosaic = Image.new("RGB", MOSAIC_SIZE, "white")

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

            # Calculate position with padding
            col = i % MOSAIC_COLS
            row = i // MOSAIC_COLS
            x = MOSAIC_PADDING + col * GLYPH_CANVAS_SIZE[0]
            y = MOSAIC_PADDING + row * GLYPH_CANVAS_SIZE[1]

            # Paste glyph into the mosaic
            mosaic.paste(glyph_img, (x, y))

        # Save the mosaic sheet
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        mosaic_path = os.path.join(OUTPUT_PATH, f"Artistic_Sheet_{sheet_idx + 1}.jpg")
        mosaic.save(mosaic_path, "JPEG")
        print(f"Saved {mosaic_path}")

# Run the artistic proof sheet generator
create_artistic_sheets()
