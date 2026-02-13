"""
Generate steganographic PAN-format hidden code image (10 chars: 4 letters + 5 digits + 1 letter).
Uses code_generator for unique, DB-backed codes when code is not provided.
"""
from PIL import Image

# ---------- CONSTANTS (must match extractor.py / revealer.py) ----------
CODE_LEN = 10
SIZE = 800
BASE_COLOR = (120, 120, 120)
RED_OFFSET = 1
GREEN_OFFSET = 1
BLUE_OFFSET = 1
DIGIT_WIDTH = 50
DIGIT_HEIGHT = 100
SPACING = 20
HALF_HEIGHT = DIGIT_HEIGHT // 2

SEGMENTS = {
    "0": ["top", "bottom", "left", "right", "diagonal_z"],
    "1": ["right"],
    "2": ["top", "middle", "bottom", "right_top", "left_bottom"],
    "3": ["top", "middle", "bottom", "right"],
    "4": ["middle", "left_top", "right"],
    "5": ["top", "middle", "bottom", "left_top", "right_bottom"],
    "6": ["top", "middle", "bottom", "left", "right_bottom"],
    "7": ["top", "right"],
    "8": ["top", "middle", "bottom", "left", "right"],
    "9": ["top", "middle", "bottom", "left_top", "right"],

    "A": ["top", "middle", "left", "right"],
    "B": ["top", "middle", "bottom", "left", "iso_b_top", "right_bottom_half"],
    "C": ["top", "bottom", "left"],
    "D": ["left", "diag_d_top", "diag_d_bottom"],
    "E": ["top", "middle", "bottom", "left"],
    "F": ["top", "middle", "left"],
    "G": ["top", "bottom", "left", "right_bottom"],
    "H": ["middle", "left", "right"],
    "I": ["top", "bottom", "center_vertical"],
    "J": ["bottom", "right"],
    "K": ["left", "diag_k_top", "diag_r_leg"],
    "L": ["bottom", "left"],
    "M": ["left", "right", "diag_m_right", "diag_y_left"],
    "N": ["left", "right", "diagonal_zero"],
    "O": ["top", "bottom", "left", "right"],
    "P": ["top", "middle", "left", "right_top"],
    "Q": ["top", "bottom", "left", "right", "diag_w_right"],
    "R": ["top", "middle", "left", "right_top_half", "diag_r_leg"],
    "S": ["top", "bottom", "diagonal_zero"],
    "T": ["top", "center_vertical"],
    "U": ["bottom", "left", "right"],
    "V": ["diag_v_right", "diag_v_left"],
    "W": ["left", "right", "diag_w_left", "diag_w_right"],
    "X": ["diagonal_z", "diagonal_zero"],
    "Y": ["diag_y_left", "diagonal_z"],
    "Z": ["top", "bottom", "diagonal_z"]
}


def _validate_code(code):
    """Validate code format: 4 letters + 5 digits + 1 letter, 10 chars total."""
    if len(code) != CODE_LEN:
        raise ValueError(f"Code must be exactly {CODE_LEN} characters")
    if not (code[:4].isalpha() and code[4:9].isdigit() and code[9].isalpha()):
        raise ValueError("Format must be: 4 letters + 5 digits + 1 letter")
    return code.upper()


def _draw_character(pixels, x_offset, char, channel, start_y):
    thickness = 6
    seg = SEGMENTS.get(char, [])

    for x in range(x_offset, x_offset + DIGIT_WIDTH):
        for y in range(start_y, start_y + DIGIT_HEIGHT):
            relative_x = x - x_offset
            relative_y = y - start_y
            draw = False

            if "top" in seg and relative_y < thickness:
                draw = True
            if "bottom" in seg and relative_y > DIGIT_HEIGHT - thickness:
                draw = True
            if "middle" in seg and HALF_HEIGHT - thickness < relative_y < HALF_HEIGHT + thickness:
                draw = True
            if "left" in seg and relative_x < thickness:
                draw = True
            if "right" in seg and relative_x > DIGIT_WIDTH - thickness:
                draw = True
            if "left_top" in seg and relative_x < thickness and relative_y < HALF_HEIGHT:
                draw = True
            if "left_bottom" in seg and relative_x < thickness and relative_y > HALF_HEIGHT:
                draw = True
            if "right_top" in seg and relative_x > DIGIT_WIDTH - thickness and relative_y < HALF_HEIGHT:
                draw = True
            if "right_bottom" in seg and relative_x > DIGIT_WIDTH - thickness and relative_y > HALF_HEIGHT:
                draw = True
            if "center_vertical" in seg and DIGIT_WIDTH // 2 - thickness < relative_x < DIGIT_WIDTH // 2 + thickness:
                draw = True
            if "right_bottom_half" in seg and relative_x > DIGIT_WIDTH - thickness and relative_y > HALF_HEIGHT:
                draw = True
            if "right_top_half" in seg and relative_x > DIGIT_WIDTH - thickness and relative_y < HALF_HEIGHT:
                draw = True

            if "diagonal_z" in seg:
                expected_x = DIGIT_WIDTH - int((relative_y * DIGIT_WIDTH) / DIGIT_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diagonal_zero" in seg:
                expected_x = int((relative_y * DIGIT_WIDTH) / DIGIT_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_r_leg" in seg and relative_y >= HALF_HEIGHT:
                adjusted = relative_y - HALF_HEIGHT
                expected_x = int((adjusted * DIGIT_WIDTH) / HALF_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_y_left" in seg and relative_y <= HALF_HEIGHT:
                expected_x = int((relative_y * (DIGIT_WIDTH // 2)) / HALF_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_m_right" in seg and relative_y <= HALF_HEIGHT:
                expected_x = DIGIT_WIDTH - int((relative_y * (DIGIT_WIDTH // 2)) / HALF_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_k_top" in seg and relative_y <= HALF_HEIGHT:
                expected_x = DIGIT_WIDTH - int((relative_y * DIGIT_WIDTH) / HALF_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_w_left" in seg and relative_y >= HALF_HEIGHT:
                adjusted = relative_y - HALF_HEIGHT
                expected_x = (DIGIT_WIDTH // 2) - int((adjusted * (DIGIT_WIDTH // 2)) / HALF_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_w_right" in seg and relative_y >= HALF_HEIGHT:
                adjusted = relative_y - HALF_HEIGHT
                expected_x = (DIGIT_WIDTH // 2) + int((adjusted * (DIGIT_WIDTH // 2)) / HALF_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_d_top" in seg and relative_y <= HALF_HEIGHT:
                expected_x = int((relative_y * DIGIT_WIDTH) / HALF_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_d_bottom" in seg and relative_y >= HALF_HEIGHT:
                adjusted = relative_y - HALF_HEIGHT
                expected_x = DIGIT_WIDTH - int((adjusted * DIGIT_WIDTH) / HALF_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_v_left" in seg:
                expected_x = int((relative_y * (DIGIT_WIDTH // 2)) / DIGIT_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True
            if "diag_v_right" in seg:
                expected_x = DIGIT_WIDTH - int((relative_y * (DIGIT_WIDTH // 2)) / DIGIT_HEIGHT)
                if abs(relative_x - expected_x) < thickness:
                    draw = True

            if draw:
                r, g, b = pixels[x, y]
                if channel == "red":
                    pixels[x, y] = (r + RED_OFFSET, g, b)
                elif channel == "blue":
                    pixels[x, y] = (r, g, b + BLUE_OFFSET)
                else:
                    pixels[x, y] = (r, g + GREEN_OFFSET, b)


def generate_hidden_code_image(code=None, output_path=None, database_url=None):
    """
    Generate the PAN-format steganographic image encoding a 10-char code.

    Args:
        code: 10-char code (4 letters + 5 digits + 1 letter). If None, a unique
              code is generated via code_generator and stored in the DB.
        output_path: Where to save the image. If None, caller must use return value.
        database_url: Passed to code_generator when code is None.

    Returns:
        tuple: (code_str, path_to_image). path_to_image is output_path if given,
               or a default path (e.g. hidden_pan_format.png in cwd) for standalone use.
    """
    if code is None:
        from code_generator import generate_unique_code
        code = generate_unique_code(database_url=database_url)

    code = _validate_code(code)

    width = height = SIZE
    img = Image.new("RGB", (width, height), BASE_COLOR)
    pixels = img.load()

    total_width = 10 * DIGIT_WIDTH + 9 * SPACING
    start_x = (width - total_width) // 2
    start_y = (height - DIGIT_HEIGHT) // 2

    for i, char in enumerate(code):
        x_position = start_x + i * (DIGIT_WIDTH + SPACING)
        if i < 5:
            _draw_character(pixels, x_position, char, "red", start_y)
        elif i < 9:
            _draw_character(pixels, x_position, char, "blue", start_y)
        else:
            _draw_character(pixels, x_position, char, "green", start_y)

    if output_path is None:
        output_path = "hidden_pan_format.png"
    img.save(output_path)
    return code, output_path


if __name__ == "__main__":
    code, path = generate_hidden_code_image()
    print(f"PAN-style hidden image created: {path} (code: {code})")
