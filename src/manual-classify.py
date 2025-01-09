import os
import shutil
import cv2 # type: ignore

# Directories
INPUT_DIR = "/home/mark/Projects/glyph-generator/data/input/glyphs-unclassified/"
OUTPUT_DIR = "/home/mark/Projects/glyph-generator/data/input/dataset"

# Classes (folders)
CLASSES = ["good", "bad"]

# Create class directories
for cls in CLASSES:
    os.makedirs(os.path.join(OUTPUT_DIR, cls), exist_ok=True)

# Get image list
images = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
current_idx = 0

while current_idx < len(images):
    img_path = os.path.join(INPUT_DIR, images[current_idx])
    img = cv2.imread(img_path)
    cv2.imshow("Image Classification", img)

    print(f"Classify: {images[current_idx]}")
    print("Press 1-2 to classify, or N to skip, Q to quit")

    key = cv2.waitKey(0)

    if key == ord('q'):
        break
    elif key == ord('n'):
        current_idx += 1
        continue
    elif chr(key).isdigit() and 1 <= int(chr(key)) <= len(CLASSES):
        cls_idx = int(chr(key)) - 1
        dest_dir = os.path.join(OUTPUT_DIR, CLASSES[cls_idx])
        shutil.move(img_path, dest_dir)
        print(f"Moved to {CLASSES[cls_idx]}")
        current_idx += 1

cv2.destroyAllWindows()
