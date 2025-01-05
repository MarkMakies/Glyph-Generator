from PIL import Image, ImageDraw
import os

# Directory containing the "bad" images
INPUT_OUTPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/random_need_mask" 

# Mask width (16 pixels along each edge)
EDGE_MASK_WIDTH = 64

def apply_edge_mask(image_path):
    """
    Applies a mask to remove white pixels from the edges of the image.
    Explicitly sets edge pixels to black and preserves the original format.
    """
    with Image.open(image_path) as img:
        # Get the original format
        original_format = img.format

        # Convert image to grayscale for simplicity (force black and white)
        img = img.convert("L")
        width, height = img.size

        # Create a mask to black out the edges
        draw = ImageDraw.Draw(img)
        # Top edge
        draw.rectangle([(0, 0), (width, EDGE_MASK_WIDTH - 1)], fill=0)
        # Bottom edge
        draw.rectangle([(0, height - EDGE_MASK_WIDTH), (width, height)], fill=0)
        # Left edge
        draw.rectangle([(0, 0), (EDGE_MASK_WIDTH - 1, height)], fill=0)
        # Right edge
        draw.rectangle([(width - EDGE_MASK_WIDTH, 0), (width, height)], fill=0)

        # Save the modified image in the same format
        if original_format == "JPEG":
            img = img.convert("RGB")  # Ensure no alpha channel for JPEGs
            img.save(image_path, format=original_format, quality=75)  # Optional: Adjust quality
        else:
            img.save(image_path, format=original_format)

        print(f"Processed and replaced: {image_path}")


def process_bad_images(path):
    """
    Process all images in the bad directory and apply the edge mask.
    """
    for file_name in os.listdir(path):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(path, file_name)
            apply_edge_mask(image_path)

# Run the script
process_bad_images(INPUT_OUTPUT_PATH)

print("Processing complete.")
