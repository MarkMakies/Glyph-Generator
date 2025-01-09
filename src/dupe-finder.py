from PIL import Image
import imagehash
import os
import shutil

# Directories
INPUT_DIRECTORY = "/home/mark/Projects/glyph-generator/data/input/glyphs-unclassified/"
DUPLICATE_DIRECTORY = "/home/mark/Projects/glyph-generator/data/output/dupes"  # Directory to move duplicates

# Ensure the duplicate directory exists
os.makedirs(DUPLICATE_DIRECTORY, exist_ok=True)

# Dictionary to store hashes and their corresponding filenames
HASHES = {}
HAMMING_THRESHOLD = 1  # Allowable Hamming distance for near-duplicates

# Loop through images and calculate perceptual hash
for filename in os.listdir(INPUT_DIRECTORY):
    filepath = os.path.join(INPUT_DIRECTORY, filename)
    if filename.endswith(".jpg"):
        img = Image.open(filepath)
        img_hash = imagehash.dhash(img)  # Use Difference Hash (dHash)

        # Check for duplicates based on Hamming distance
        duplicate_found = False
        for existing_hash, files in HASHES.items():
            if img_hash - existing_hash <= HAMMING_THRESHOLD:  # Compare Hamming distance
                duplicate_found = True
                original_filename = files[0]
                original_filepath = os.path.join(INPUT_DIRECTORY, original_filename)
                duplicate_filepath = filepath

                # Move the original file to the duplicate directory (if not already moved)
                if not files[1]:
                    shutil.move(original_filepath, os.path.join(DUPLICATE_DIRECTORY, original_filename))
                    files[1] = True  # Mark as moved

                # Move the duplicate file
                shutil.move(duplicate_filepath, os.path.join(DUPLICATE_DIRECTORY, filename))

                # Determine a unique name for the duplicate
                duplicate_count = len(files) - 1  # Count existing duplicates
                new_name = original_filename.replace(".jpg", f"_{duplicate_count}.jpg")
                os.rename(
                    os.path.join(DUPLICATE_DIRECTORY, filename),
                    os.path.join(DUPLICATE_DIRECTORY, new_name),
                )

                print(f"Duplicate found (Hamming distance {img_hash - existing_hash}): {original_filename} and renamed {filename} to {new_name}")

                # Add the new duplicate to the hash entry
                files.append(new_name)
                break

        # If no duplicates found, add hash to HASHES
        if not duplicate_found:
            HASHES[img_hash] = [filename, False]  # [original_filename, is_moved_flag]
