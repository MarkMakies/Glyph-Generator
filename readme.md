# Glyph Generator

The **Glyph Generator** project began as an effort to create visually compelling glyphs for the Glow Cuboid, leveraging AI to assist with random generation, classification, and artistic processing. However, it has now evolved into a standalone system for glyph generation, including random glyph creation, extracting glyphs from Unicode fonts, machine learning-based classification, and applying artistic transformations to create captivating outputs.

This system is modular and can be used for artistic, functional, or experimental purposes, such as creating custom art or visualizations.

![Artistic Glyph Example](images/Artistic-Sheet-1.jpg)

---

## Features
1. **Random Glyph Generation**: Generate millions of random glyphs with 16x16 cells.
2. **Font-Based Glyph Extraction**: Extract glyphs from Unicode fonts and convert them to a 14x14 grid with padding.
3. **Machine Learning Classification**: Train an ML model to classify glyphs as "good" or "bad."
4. **Proof Sheet Creation**: Generate organized glyph sheets for review or art projects.
5. **Artistic Processing**: Transform glyphs into visually stunning designs using Gaussian blur and other artistic effects.

---

## How to Use
### Step-by-Step Guide
1. **Create Random Glyphs**:
   - Use `create-random-glyphs.py` to generate up to 1,000,000 random glyphs. These glyphs are initially created in a 16x16 B/W format, upscaled to 128x128 RGB JPGs.

2. **Optionally Generate Glyphs from Fonts**:
   - Use `create-unicode-glyphs.py` to extract glyphs from system-installed fonts. The glyphs are created on a 14x14 grid with a 1-cell black padding around the edges (16x16 canvas).

3. **Randomly Rename Files**:
   - Use `file-random-rename.py` to randomize file names. This is particularly useful to ensure glyphs appear in a random order when generating proof sheets.

4. **Train the ML Model**:
   - Use `train.py` to train a machine learning model. Start with manually classified images (you can use `manual-classify.py` to help with this):
     - At least 1,000 "good" glyphs (e.g., from font-based generation).
     - At least 1,000 "bad" glyphs (e.g., random glyphs).
   - Train the model with low epochs (e.g., 3) to avoid overfitting.
   - Save the trained model
   - check result charts to ensure validation accuracy is good. 

5. **Classify Glyphs Automatically**:
   - Use `auto-classify-directory.py` to classify glyphs based on the trained model. Glyphs are moved into "good" or "bad" directories based on a classification threshold (e.g., 99% probability).
   - To ensure that no two are too alike, use `dupe-finder.py` to cull some.

6. **Generate Proof Sheets**:
   - **Basic Proof Sheets**: Use `create-basic-sheets.py` to create simple proof sheets with a consistent grid layout.
   - **Artistic Sheets**: Use `create-artistic-sheets.py` to upscale glyphs, apply artistic filters (Gaussian blur, Difference of Gaussians, etc.), and generate visually compelling sheets.

---

## Source Code Overview

### Glyph Creation
#### `create-random-glyphs.py`
- Generates random glyphs with 16x16 B/W cells.
- Automatically upscales glyphs to 128x128 RGB JPGs.

#### `create-unicode-glyphs.py`
- Extracts glyphs from system-installed fonts.
- Generates glyphs on a 14x14 grid with a 16x16 canvas (1-cell padding around edges).

---

### File Management
#### `file-random-rename.py`
- Renames glyph files randomly with a configurable naming mask (e.g., `G-123abc.jpg`).
- Ensures filenames are unique and preserves file format.

---

### Machine Learning
#### `train.py`
- Uses manually classified datasets (`good` and `bad` directories) to train a model for glyph classification.
- Tips:
  - Use extracted font-based glyphs for "good" data and random glyphs for "bad" data.
  - Low epochs (e.g., 3) work best to prevent overfitting.  Observe charts at end of process, if validation rates start falling your epochs is set too high.
  - Retrain iteratively to refine classification accuracy.

#### `auto-classify-directory.py`
- Uses the trained model to classify glyphs with high confidence (e.g., 99% probability).
- Moves classified glyphs into "good" or "bad" directories.

---

### Proof Sheet Generation
#### `create-basic-sheets.py`
- Generates simple proof sheets with consistent glyph spacing.
- Each glyph is mapped 1:1 to its original size and format.

#### `create-artistic-sheets.py`
- Upscales glyphs (128x128 → 512x512) and applies artistic effects:
  - Gaussian blur
  - Smoothing
  - Difference of Gaussians filter
- Includes options for customizable padding, rotations, and downscaling.

---

## Example Workflow
```bash
# 1. Generate 1,000,000 random glyphs
python create-random-glyphs.py

# 2. Optionally generate glyphs from fonts
python create-unicode-glyphs.py

# 3. Randomly rename glyph files
python file-random-rename.py

# 4. Train ML model with manually classified glyphs
python train.py

# 5. Classify glyphs automatically
python auto-classify-directory.py

# 6. Create proof sheets
python create-basic-sheets.py

# 7. Generate artistic sheets
python create-artistic-sheets.py
```

## Tips for Success

**Proof Sheets:** Use proof sheets to visually inspect glyph quality and classification results.

**Model Retraining:** Iteratively improve the ML model by adding more classified glyphs to the training dataset.

**Customization:** Modify artistic effects and proof sheet layouts to match your creative vision.

## Future Directions

This project demonstrates how AI can aid in artistic creation. Potential future expansions include:

  * Generating glyphs using generative adversarial networks (GANs).
  * Creating interactive tools for customizing glyph styles.
  * Expanding the dataset to include glyphs from more fonts and languages.