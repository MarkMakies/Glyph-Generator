import os
import random
import string

# Constants
INPUT_DIRECTORY = "/home/mark/Projects/Glow Cuboid/Glyphs/Unicode_Selected"
FILE_PREFIX = 'G-'
FILE_SUFFIX = '-U.jpg'
FILE_MASK = 'DDDDDDDD'  # File name structure: D = digit, L = letter

def generate_random_name(mask, prefix, suffix, existing_names):
    """Generate a unique random file name based on the given mask."""
    while True:
        # Create a random name based on the mask
        random_name = ''.join(
            random.choice(string.digits) if char == 'D' else random.choice(string.ascii_lowercase)
            for char in mask
        )
        full_name = f"{prefix}{random_name}{suffix}"
        if full_name not in existing_names:
            return full_name

def rename_files_in_directory(input_dir, file_prefix, file_suffix, file_mask):
    """Rename all files in the given directory randomly based on the mask."""
    existing_names = set(os.listdir(input_dir))  # Track existing file names to ensure uniqueness

    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if os.path.isfile(file_path):  # Only process files, not directories
            new_name = generate_random_name(file_mask, file_prefix, file_suffix, existing_names)
            new_path = os.path.join(input_dir, new_name)
            os.rename(file_path, new_path)
            print(f"Renamed: {file_name} -> {new_name}")
            existing_names.add(new_name)  # Add the new name to the set

# Run the renaming process
rename_files_in_directory(INPUT_DIRECTORY, FILE_PREFIX, FILE_SUFFIX, FILE_MASK)

