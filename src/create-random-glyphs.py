from random import randint as RI, choice
from collections import deque
from PIL import Image

# Constants
OUTPUT_PATH = "/home/mark/Projects/Glyph Generator/data/output/random" 

NUM_PIXELS = 256
GRID_SIZE = 16
MIN_LEVEL = 0
MAX_LEVEL = 256

CLUSTER_SIZE = 8  # Define cluster size. Isolated clusters less than this size are removed
MIN_NUM_STROKES = 5
MAX_NUM_STROKES = 10

MIN_STROKE_LENGTH = 8
MAX_STROKE_LENGTH = 40

PROB_CURVED_STROKE = 95

PROB_BRANCHING = 80
PROB_VERT_SYM = 30
PROB_HORIZ_SYM = 30
PROB_DIAG_SYM = 30

MAX_DOTS = 0
MIN_PIXELS_ON = 8
MAX_PIXELS_ON = 48

PIXEL_SIZE = 8  # Size of each pixel in output images
PIXEL_PADDING = 0  # Padding size in pixels

def reset_buffers():
    return [0] * NUM_PIXELS, [0] * NUM_PIXELS, [0] * NUM_PIXELS, [False] * NUM_PIXELS, [0] * NUM_PIXELS

def generate_glyph():
    r, g, b, on, _ = reset_buffers()

    def activate_pixel(pixel, color=None):
        if not color:
            color = (RI(MIN_LEVEL, MAX_LEVEL), RI(MIN_LEVEL, MAX_LEVEL), RI(MIN_LEVEL, MAX_LEVEL))
        r[pixel], g[pixel], b[pixel] = color
        on[pixel] = True

    def draw_stroke(start_pixel, direction, length):
        current_pixel = start_pixel
        for _ in range(length):
            if 0 <= current_pixel < NUM_PIXELS and not on[current_pixel]:
                activate_pixel(current_pixel)
                row, col = divmod(current_pixel, GRID_SIZE)
                if direction == "up" and row > 0:
                    current_pixel -= GRID_SIZE
                elif direction == "down" and row < GRID_SIZE - 1:
                    current_pixel += GRID_SIZE
                elif direction == "left" and col > 0:
                    current_pixel -= 1
                elif direction == "right" and col < GRID_SIZE - 1:
                    current_pixel += 1
                elif direction == "up-right" and row > 0 and col < GRID_SIZE - 1:
                    current_pixel -= (GRID_SIZE - 1)
                elif direction == "up-left" and row > 0 and col > 0:
                    current_pixel -= (GRID_SIZE + 1)
                elif direction == "down-right" and row < GRID_SIZE - 1 and col < GRID_SIZE - 1:
                    current_pixel += (GRID_SIZE + 1)
                elif direction == "down-left" and row < GRID_SIZE - 1 and col > 0:
                    current_pixel += (GRID_SIZE - 1)
                else:
                    break
            else:
                break

    def draw_curve(start_pixel, direction):
        """Draws a curve starting at the given pixel and following the specified direction."""
        row, col = divmod(start_pixel, GRID_SIZE)
        curve_offsets = []
        
        # Define curve patterns based on the initial direction
        if direction == "up-right":
            curve_offsets = [(-1, 0), (-1, 1), (0, 1), (1, 1)]  # Makes a gentle "arc"
        elif direction == "down-right":
            curve_offsets = [(1, 0), (1, 1), (0, 1), (-1, 1)]  # Another smooth arc
        elif direction == "down-left":
            curve_offsets = [(1, 0), (1, -1), (0, -1), (-1, -1)]
        elif direction == "up-left":
            curve_offsets = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
        elif direction == "vertical":
            curve_offsets = [(-1, 0), (-2, 0), (-1, 1), (-1, -1)]  # Vertical arc
        elif direction == "horizontal":
            curve_offsets = [(0, 1), (0, 2), (1, 1), (-1, 1)]  # Horizontal arc

        for dr, dc in curve_offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                pixel = nr * GRID_SIZE + nc
                if not on[pixel]:
                    activate_pixel(pixel)
                    row, col = nr, nc

    # Generate strokes and curves
    def gen_strokes():
        num_strokes = RI(MIN_NUM_STROKES, MAX_NUM_STROKES)
        for _ in range(num_strokes):
            start_pixel = RI(0, NUM_PIXELS - 1)
            direction = choice(["up", "down", "left", "right", "up-right", "up-left", "down-right", "down-left", "vertical", "horizontal"])
            stroke_type = "curve" if RI(1, 100) <= PROB_CURVED_STROKE else "straight"

            stroke_length = RI(MIN_STROKE_LENGTH, MAX_STROKE_LENGTH)

            if stroke_type == "straight":
                draw_stroke(start_pixel, direction, stroke_length)
            elif stroke_type == "curve":
                draw_curve(start_pixel, direction)

            if RI(1, 100) <= PROB_BRANCHING:  
                branch_direction = choice(["up", "down", "left", "right", "up-right", "up-left", "down-right", "down-left", "vertical", "horizontal"])
                draw_stroke(start_pixel, branch_direction, RI(2, 4))

    # Apply Symmetry
    def apply_symmetry():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                current_pixel = row * GRID_SIZE + col
                if on[current_pixel]:
                    if RI(1, 100) <= PROB_VERT_SYM:
                        vertical_pixel = row * GRID_SIZE + (GRID_SIZE - 1 - col)
                        activate_pixel(vertical_pixel, color=(r[current_pixel], g[current_pixel], b[current_pixel]))
                    if RI(1, 100) <= PROB_HORIZ_SYM:
                        horizontal_pixel = (GRID_SIZE - 1 - row) * GRID_SIZE + col
                        activate_pixel(horizontal_pixel, color=(r[current_pixel], g[current_pixel], b[current_pixel]))
                    if RI(1, 100) <= PROB_DIAG_SYM:
                        diagonal_pixel = col * GRID_SIZE + row
                        activate_pixel(diagonal_pixel, color=(r[current_pixel], g[current_pixel], b[current_pixel]))

    # Ensure min and max pixel count
    def check_count():
        on_pixels = [i for i in range(NUM_PIXELS) if on[i]]
        if len(on_pixels) < MIN_PIXELS_ON:
            while len(on_pixels) < MIN_PIXELS_ON:
                activate_pixel(RI(0, NUM_PIXELS - 1))
                on_pixels = [i for i in range(NUM_PIXELS) if on[i]]
        elif len(on_pixels) > MAX_PIXELS_ON:
            while len(on_pixels) > MAX_PIXELS_ON:
                pixel_to_deactivate = choice(on_pixels)
                r[pixel_to_deactivate] = g[pixel_to_deactivate] = b[pixel_to_deactivate] = 0
                on[pixel_to_deactivate] = False
                on_pixels.remove(pixel_to_deactivate)

    # Remove clusters smaller than or equal to CLUSTER_SIZE
    def remove_small_clusters():
        visited = [False] * NUM_PIXELS

        def bfs(start_pixel):
            """Breadth-first search to find all pixels in a cluster, including diagonal neighbors."""
            queue = deque([start_pixel])
            cluster = []
            while queue:
                pixel = queue.popleft()
                if not visited[pixel]:
                    visited[pixel] = True
                    cluster.append(pixel)
                    row, col = divmod(pixel, GRID_SIZE)
                    # Add all 8 possible neighbors (horizontal, vertical, diagonal)
                    neighbors = [
                        (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),  # Horizontal/vertical
                        (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)  # Diagonal
                    ]
                    for nr, nc in neighbors:
                        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                            neighbor_pixel = nr * GRID_SIZE + nc
                            if on[neighbor_pixel] and not visited[neighbor_pixel]:
                                queue.append(neighbor_pixel)
            return cluster

        for pixel in range(NUM_PIXELS):
            if on[pixel] and not visited[pixel]:
                cluster = bfs(pixel)
                if len(cluster) <= CLUSTER_SIZE:
                    for p in cluster:
                        on[p] = False
                        r[p], g[p], b[p] = 0, 0, 0

    # Add occasional isolated pixels
    def add_isolated():
        for _ in range(RI(0, MAX_DOTS)):
            isolated_pixel = RI(0, NUM_PIXELS - 1)
            if not on[isolated_pixel]:
                activate_pixel(isolated_pixel)

    def center_glyph(r, g, b, on):
        """Centers the glyph in the grid."""
        # Determine the bounding box
        rows = [pixel // GRID_SIZE for pixel in range(NUM_PIXELS) if on[pixel]]
        cols = [pixel % GRID_SIZE for pixel in range(NUM_PIXELS) if on[pixel]]

        if not rows or not cols:  # If no pixels are "on," no need to center
            return r, g, b, on

        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        glyph_height = max_row - min_row + 1
        glyph_width = max_col - min_col + 1

        # Calculate the offset needed to center the glyph
        row_offset = (GRID_SIZE - glyph_height) // 2 - min_row
        col_offset = (GRID_SIZE - glyph_width) // 2 - min_col

        # Create new buffers
        new_r, new_g, new_b, new_on, _ = reset_buffers()

        for pixel in range(NUM_PIXELS):
            if on[pixel]:
                row, col = divmod(pixel, GRID_SIZE)
                new_row = row + row_offset
                new_col = col + col_offset

                if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                    new_pixel = new_row * GRID_SIZE + new_col
                    new_r[new_pixel] = r[pixel]
                    new_g[new_pixel] = g[pixel]
                    new_b[new_pixel] = b[pixel]
                    new_on[new_pixel] = True

        return new_r, new_g, new_b, new_on
            
    gen_strokes()

    apply_symmetry()
    remove_small_clusters()
    #check_count()
    #add_isolated()
    r, g, b, on = center_glyph(r, g, b, on)

    return r, g, b

def matrix_to_image(r, g, b, output_file="output.png"):
    """Converts RGB buffers to an image with padding and saves it."""
    matrix = [
        [(r[row * GRID_SIZE + col], g[row * GRID_SIZE + col], b[row * GRID_SIZE + col])
         for col in range(GRID_SIZE)]
        for row in range(GRID_SIZE)
    ]
    # Calculate the size of the image, accounting for padding
    padded_pixel_size = PIXEL_SIZE + PIXEL_PADDING
    img_size = GRID_SIZE * padded_pixel_size - PIXEL_PADDING  # Avoid extra padding at the edges
    img = Image.new("RGB", (img_size, img_size), "black")

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = matrix[row][col]
            if row == 0 or row == GRID_SIZE-1 or col==0 or col==GRID_SIZE-1:    # no pixels at
                color = (0,0,0)
            if color != (0,0,0): 
                color = (255,255,255)
            # Top-left corner of the "pixel" area
            x_start = col * padded_pixel_size
            y_start = row * padded_pixel_size
            for x in range(PIXEL_SIZE):
                for y in range(PIXEL_SIZE):
                    img.putpixel((x_start + x, y_start + y), color)

    img.save(output_file)
    print(f"Image saved to {output_file}")

# Generate and save multiple glyphs
for i in range(100):

    CLUSTER_SIZE = RI(4,16)
    MIN_NUM_STROKES = RI(2,10)
    MAX_NUM_STROKES = RI(MIN_NUM_STROKES+1,MIN_NUM_STROKES+10)

    MIN_STROKE_LENGTH = RI(4,16)
    MAX_STROKE_LENGTH = RI(MIN_STROKE_LENGTH+1,MIN_STROKE_LENGTH+10)

    PROB_CURVED_STROKE = RI(30,100)

    PROB_BRANCHING = RI(20,50)
    PROB_VERT_SYM = RI(10,50)
    PROB_HORIZ_SYM = RI(10,50)
    PROB_DIAG_SYM = RI(10,50)

    r, g, b = generate_glyph()
    matrix_to_image(r, g, b, output_file=f"{OUTPUT_PATH}/G_{i}.jpg")
