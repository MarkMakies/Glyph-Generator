### Capture Environment

List what I have installed
  * ``` pip list --not-required ``` 

Save all installed libraries (explicit and dependencies)
  * ``` pip freeze > requirements.txt ``` 
### Setup Environment

VSC create virtual environment
  * ```ctl+shft+P -> create environment```
  
Install all dependencies at once
  * ```pip install -r requirements.txt``` 

### using GIT
cd to_project_dir
git init

git branch -m main


**Track changes / staging files**
git add src
git add notes.md
git add requirements.txt 

**Commit changes**
git commit -m "Just copied accross from Glow Cuboid directory"


git status
git log

git add .gitignore
git commit -m "Added .gitignore file"


git add fname to get it into staging area
git commit to save all those staged into repository



git checkout main  - make sure we are on the main branch repository -> working directory

git checkout -b color-experiment   - creates a new branch and switches to it
- Edit files, then stage them:
git add colorize_glyphs.py
- Commit the changes:
git add .
git commit -m "Added initial colorizing code for experiment"

If it works, switch to main branch and merge

git checkout main
git merge color-experiment
Clean Up the Experimental Branch
git branch -d color-experiment

If It Doesn’t Work: Discard the Experiment

git checkout main
git branch -D color-experiment
Start Fresh: Your main branch is untouched and remains in its stable state.


Action  | 	Command
---|---
Create a new branch	| git checkout -b branch-name
Switch branches |	git checkout branch-name
Stage changes	| git add .
Commit changes |	git commit -m "Commit message"
Merge a branch into main |	git merge branch-name
Delete a branch (merged) |	git branch -d branch-name
Delete a branch (unmerged) |	git branch -D branch-name



---
### Source Code

#### create-random-glyphs.py
* Generates 16x16 cells B/W random cells.  
    * modified to create 14x14 with one cell padding all around *
* Upsample at 8 pixels per cell so 16x16 becomes 128x128 jpgs

#### create_basic_sheets.py
* creates a basic proof sheet
* one to one mapping for glyph size, format

#### create-artistic-sheets.py
* upscales by 4x (128 -> 512) first
* applies Gaussian blur and smoothing
* then applies Difference of Gaussians filter, Mait figured it out from GIMP workflow

#### edge_mask.py
* was used to remove edge pixels to get 16x16 to 14x14 , NOT NEEDED anymore

#### white-edge-detection.py
* was used to identify those glyphs which had a white edge , NOT NEEDED anymore

#### train.py
* use manually classified 'good' and 'bad' directories under dataset path to train model
```model.save("glyph_classifier3.keras")```
*  epochs - a low number works best to prevent overfitting

#### auto-classify-directory.py
* use model to automatically classify with a probability of 99% 'good' and **move** into appropriate directories

#### generate_unicode_glyphs.py
* use to create multiple 14x14 glyphs on a 16x16 canvas to replicate the random_generation function.

#### file_random_rename.py
* use to randomise file names, especially for fonts, so that proof sheets use glyphs in a random order.

#### colourize.py
**WIP** 

#### compressor.py
**WIP** to use these 'basic' B/W glyphs later on MCU  

---
### Training
* first used manual classification, 1k good, 2k bad
* subsequently used extracted fonts to re-train with more good, whilst copying random to bad dataset (as most of htese (<1% ) would be good in anyu case)



## To try

```
import os

# Paths to scripts
create_glyphs_script = "src/create_glyphs.py"
colourize_glyphs_script = "src/colourize_glyphs.py"

# Run the scripts in sequence
os.system(f"python {create_glyphs_script}")
os.system(f"python {colourize_glyphs_script}")
print("Workflow completed!")
```

```
python workflow.py
```


---
---
---

# EXAMPLES of .MD

[I'm an inline-style link](https://www.google.com)


1. First ordered list item
2. Another item
⋅⋅* Unordered sub-list. 
1. Actual numbers don't matter, just that it's a number
⋅⋅1. Ordered sub-list
4. And another item.

⋅⋅⋅You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

⋅⋅⋅To have a line break without a paragraph, you will need to use two trailing spaces.⋅⋅
⋅⋅⋅Note that this line is separate, but within the same paragraph.⋅⋅
⋅⋅⋅(This is contrary to the typical GFM line break behaviour, where trailing spaces are not required.)

* Unordered list can use asterisks
- Or minuses
+ Or pluses

Inline-style: 
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")


```python
s = "Python syntax highlighting"
print s
```
Here is a simple footnote[^1].

A footnote can also have multiple lines[^2].  

You can also use words, to fit your writing style more closely[^note].

[^1]: My reference.
Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3


> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote. Three or more...

---

Hyphens

***

Asterisks

___

Underscores



Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.