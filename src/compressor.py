

"""
Glyph Image Compressor to run on PC
Take each image file in GLYPH_DIR and convert to a binary representation (B&W only)
which will be NUM_PIXELS / 8 bytes in size.  So for an 8x8 array, 32 byte result
Create a binary file and append each represenation 
"""

from PIL import Image
import os
import struct

GLYPH_DIR = "/home/mark/Projects/Glow Cuboid/picsBW_good"
COMPRESSED_GLYPHS = "/home/mark/Projects/Glow Cuboid/GlyphV1.bin"
PIXEL_SIZE = 8  # Glyphs are 8x8
NUM_PIXELS = PIXEL_SIZE * PIXEL_SIZE  # Total number of pixels in a glyph
BYTES_PER_GLYPH = NUM_PIXELS // 8  # 32 bytes per glyph for an 8x8 grid

def compress_glyphs():
    glyph_files = [f for f in os.listdir(GLYPH_DIR) if f.endswith(".jpg")]
    with open(COMPRESSED_GLYPHS, "wb") as output_file:
        for glyph_file in glyph_files:
            glyph_path = os.path.join(GLYPH_DIR, glyph_file)
            glyph_img = Image.open(glyph_path).convert("1")  # Convert to black and white (1-bit per pixel)
            glyph_data = glyph_img.resize((PIXEL_SIZE, PIXEL_SIZE)).getdata()

            # Encode the glyph as binary data (8 pixels per byte)
            byte_array = []
            for i in range(0, NUM_PIXELS, 8):
                byte = 0
                for j in range(8):
                    bit = 1 if glyph_data[i + j] > 0 else 0
                    byte = (byte << 1) | bit
                byte_array.append(byte)

            # Write the binary representation to the file
            output_file.write(struct.pack(f"{BYTES_PER_GLYPH}B", *byte_array))
            print(f"Compressed {glyph_file}")

compress_glyphs()


"""
Glyph Image uncompressor to run on MCU
First calculate number of 'glyph represenations' in the file, NUM_GLYPHS = ?
Then create a function to read the represenation of a singe glyph, for example

glyph_code = read_glyph(COMPRESSED_GLYPHS, RandomInt(0, NUM_GLYPHS-1)), 
in this case we would expect a return of 256 bits (32 byte boundary)
I'll then colourise and display on LED matrix for a random period, whilst fetching the next one.
The file will end up being in the MBs so can't load into memory
glyph_code - there is probably a better way to do this rather than a list, but I'm not sure how.  
All I need to do is iterate through all 256 pixels to see if they are on or off 
"""

NUM_PIXELS = 256  # Total number of pixels per glyph
BYTES_PER_GLYPH = NUM_PIXELS // 8  # 32 bytes per glyph
COMPRESSED_GLYPHS_FILE = "/home/mark/Projects/Glow Cuboid/GlyphV1.bin"

def read_glyph(file_path, index):
    """Read and decompress a single glyph from the binary file."""
    with open(file_path, "rb") as f:
        # Seek to the start of the glyph's data
        f.seek(index * BYTES_PER_GLYPH)
        glyph_bytes = f.read(BYTES_PER_GLYPH)

    # Convert bytes back to binary (pixel data)
    glyph_code = []
    for byte in glyph_bytes:
        for i in range(8):
            glyph_code.append((byte >> (7 - i)) & 1)
    return glyph_code

# Example MCU Loop
from time import sleep
from random import randint

def run_mcu_simulation():
    with open(COMPRESSED_GLYPHS_FILE, "rb") as f:
        f.seek(0, 2)  # Go to the end of the file
        file_size = f.tell()
        NUM_GLYPHS = file_size // BYTES_PER_GLYPH

    while True:
        # Fetch a random glyph
        glyph_code = read_glyph(COMPRESSED_GLYPHS_FILE, randint(0, NUM_GLYPHS - 1))

        # Simulate rendering the glyph (example only)
        print(f"Displaying Glyph: {glyph_code[:16]}...")  # Show part of the glyph for debugging
        sleep(randint(500, 1500) / 1000)  # Simulate random display time

run_mcu_simulation()

