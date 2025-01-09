from PIL import Image, ImageDraw, ImageFont
import unicodedata

# Constants
UNICODE_FONT = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
OUTPUT_DIR = "/home/mark/Projects/glyph-generator/data/input/glyphs-unclassified/"

UNICODE_START = 0x0021
UNICODE_END = 0x02a7
GRID_SIZE = 16
GLYPH_SIZE = 14
PIXEL_SIZE = 8
PIXEL_PADDING = 0  # Padding size in pixels

def center_glyph(binary_array):
    """Centers a binary glyph in a 16x16 grid."""
    rows = [i // GRID_SIZE for i, val in enumerate(binary_array) if val == 1]
    cols = [i % GRID_SIZE for i, val in enumerate(binary_array) if val == 1]
    
    if not rows or not cols:  # If no pixels are "on," return as is
        return binary_array

    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    glyph_height = max_row - min_row + 1
    glyph_width = max_col - min_col + 1

    row_offset = (GRID_SIZE - glyph_height) // 2 - min_row
    col_offset = (GRID_SIZE - glyph_width) // 2 - min_col

    centered_array = [0] * (GRID_SIZE * GRID_SIZE)
    for i, val in enumerate(binary_array):
        if val == 1:
            row, col = divmod(i, GRID_SIZE)
            new_row, new_col = row + row_offset, col + col_offset
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                centered_array[new_row * GRID_SIZE + new_col] = 1

    return centered_array

def unicode_to_image(unicode_char, font, output_file):
    """Converts a Unicode character to a 16x16 binary glyph image and saves it."""
    # Create a blank 14x14 image for the glyph
    glyph_size = GLYPH_SIZE
    img = Image.new("L", (glyph_size, glyph_size), color=0)  # Black background
    draw = ImageDraw.Draw(img)

    # Draw the Unicode character
    draw.text((0, 0), unicode_char, fill=255, font=font)  # No offset for perfect centering

    # Convert the image to a binary array
    binary_array = [1 if img.getpixel((x, y)) > 128 else 0 for y in range(glyph_size) for x in range(glyph_size)]

    # Expand to 16x16 and center the glyph
    expanded_array = [0] * (GRID_SIZE * GRID_SIZE)
    for y in range(glyph_size):
        for x in range(glyph_size):
            expanded_array[(y + 1) * GRID_SIZE + (x + 1)] = binary_array[y * glyph_size + x]

    centered_array = center_glyph(expanded_array)

    # Convert the binary array to a 16x16 image
    img_16x16 = Image.new("L", (GRID_SIZE, GRID_SIZE), color=0)
    for i, val in enumerate(centered_array):
        if val == 1:
            img_16x16.putpixel((i % GRID_SIZE, i // GRID_SIZE), 255)

    # Upscale to 128x128 RGB
    upscale_size = GRID_SIZE * (PIXEL_SIZE + PIXEL_PADDING) - PIXEL_PADDING
    img_128x128 = img_16x16.resize((upscale_size, upscale_size), resample=Image.NEAREST).convert("RGB")

    # Save the image
    img_128x128.save(output_file)
    print(f"Saved: {output_file}")

def is_printable(char):
    """Checks if a Unicode character is printable."""
    try:
        # Unicode categories for printable characters
        category = unicodedata.category(char)
        # Exclude control characters (Cc), format (Cf), surrogates (Cs), private use (Co), and unassigned (Cn)
        return not category.startswith(('C'))  # Excludes all control categories
    except ValueError:
        # In case of invalid Unicode characters
        return False


def generate_unicode_glyphs():
    """Generates glyphs for a range of Unicode characters, excluding non-printable ones."""
    font = ImageFont.truetype(UNICODE_FONT, size=12)  # Load the font with size 12
    for codepoint in range(UNICODE_START, UNICODE_END + 1):
        unicode_char = chr(codepoint)
        if is_printable(unicode_char):  # Check if the character is printable
            output_file = f"{OUTPUT_DIR}/Unicode_unifont_{codepoint}.jpg"
            unicode_to_image(unicode_char, font, output_file)
        else:
            print(f"Skipped non-printable character: U+{codepoint:04X}")

# Generate Unicode glyphs
generate_unicode_glyphs()
