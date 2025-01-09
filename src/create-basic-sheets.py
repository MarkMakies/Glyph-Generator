from PIL import Image, ImageDraw, ImageFont
import os
import math

# Parameters
INPUT_PATH = "/home/mark/Projects/glyph-generator/data/output/glyphs" 
OUTPUT_PATH = "/home/mark/Projects/glyph-generator/data/output/sheets" 

GLYPH_CANVAS_SIZE = (128, 128)  # Size for each glyph's canvas
MOSAIC_ROWS = 48  # Number of rows in the mosaic
MOSAIC_COLS = 64  # Number of columns in the mosaic
MOSAIC_PADDING = 16  # Padding between glyphs and edges of the mosaic (in pixels)

# Automatically calculate MOSAIC_SIZE
MOSAIC_SIZE = (
    MOSAIC_COLS * GLYPH_CANVAS_SIZE[0] + (MOSAIC_PADDING * 2),
    MOSAIC_ROWS * GLYPH_CANVAS_SIZE[1] + (MOSAIC_PADDING * 2),
)

def create_proof_sheets():
    glyph_files = [f for f in os.listdir(INPUT_PATH) if f.endswith(".jpg")]
    glyph_count = len(glyph_files)
    glyphs_per_sheet = MOSAIC_ROWS * MOSAIC_COLS

    # Number of sheets needed
    num_sheets = math.ceil(glyph_count / glyphs_per_sheet)

    print(f"Generating {num_sheets} mosaic sheets...")

    for sheet_idx in range(num_sheets):
        # Create a blank mosaic with padding
        mosaic = Image.new("RGB", MOSAIC_SIZE, "black")

        for i in range(glyphs_per_sheet):
            glyph_idx = sheet_idx * glyphs_per_sheet + i
            if glyph_idx >= glyph_count:
                break

            glyph_path = os.path.join(INPUT_PATH, glyph_files[glyph_idx])
            glyph_img = Image.open(glyph_path).resize(GLYPH_CANVAS_SIZE, Image.LANCZOS)

            # Calculate position with padding
            col = i % MOSAIC_COLS
            row = i // MOSAIC_COLS
            x = MOSAIC_PADDING + col * GLYPH_CANVAS_SIZE[0]
            y = MOSAIC_PADDING + row * GLYPH_CANVAS_SIZE[1]

            mosaic.paste(glyph_img, (x, y))

        # Save the mosaic sheet
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        mosaic_path = os.path.join(OUTPUT_PATH, f"Basic_Sheet_{sheet_idx + 1}.jpg")
        mosaic.save(mosaic_path, "PNG")
        print(f"Saved {mosaic_path}")

# Run the proof sheet generator
create_proof_sheets()
