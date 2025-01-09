import os
import shutil
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore

# Parameters
MODEL_PATH = "/home/mark/Projects/glyph-generator/data/models/glyph-classifier3.keras"  # Path to the trained model
INPUT_DIRECTORY = "/home/mark/Projects/glyph-generator/data/output/random"   # Directory with images to classify
GOOD_DIR = "/home/mark/Projects/glyph-generator/data/output/glyphs"  # Directory for classified 'good' images
BAD_DIR = "/home/mark/Projects/glyph-generator/data/output/bad-glyphs"    # Directory for classified 'bad' images
IMAGE_SIZE = (128, 128)   # Input image size used for training (height and width)

# Load the trained model
model = load_model(MODEL_PATH)

from tensorflow.keras.optimizers import Adam # type: ignore
# Compile the loaded model (optional but recommended)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Ensure output directories exist
os.makedirs(GOOD_DIR, exist_ok=True)
os.makedirs(BAD_DIR, exist_ok=True)

# Function to classify a single image
def classify_image(image_path):
    # Load and preprocess the image
    img = load_img(image_path, target_size=IMAGE_SIZE)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize to [0, 1]
    
    # Predict using the model
    prediction = model.predict(img_array)
    print(f"Prediction for {image_path}: {prediction}")  # Debug: log the prediction probabilities
    return 1 if prediction >= 0.95 else 0
    #return np.argmax(prediction)  # Returns 0 for 'bad', 1 for 'good'

# Classify all images in the input directory
for filename in os.listdir(INPUT_DIRECTORY):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Ensure valid image files
        file_path = os.path.join(INPUT_DIRECTORY, filename)
        result = classify_image(file_path)
        
        if result == 1:  # 'Good' classification
            shutil.move(file_path, os.path.join(GOOD_DIR, filename))
        else:  # 'Bad' classification
            shutil.move(file_path, os.path.join(BAD_DIR, filename))

print("Classification complete. Images moved to 'good' and 'bad' directories.")
