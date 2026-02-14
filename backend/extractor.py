from PIL import Image
import numpy as np
import os

# ===============================
# SETTINGS (MUST MATCH ENCODER)
# ===============================
digit_width = 50
digit_height = 100
spacing = 20
base_color = 120
TOTAL_CHARACTERS = 10
thickness = 6
half_height = digit_height // 2

# ===============================
# SEGMENT DEFINITIONS (FROM ENCODER)
# ===============================
segments = {
    "0": ["top", "bottom", "left", "right", "diagonal_z"],
    "1": ["right"],
    "2": ["top","middle","bottom","right_top","left_bottom"],
    "3": ["top","middle","bottom","right"],
    "4": ["middle","left_top","right"],
    "5": ["top","middle","bottom","left_top","right_bottom"],
    "6": ["top","middle","bottom","left","right_bottom"],
    "7": ["top","right"],
    "8": ["top","middle","bottom","left","right"],
    "9": ["top","middle","bottom","left_top","right"],

    "A": ["top","middle","left","right"],
    "B": ["top","middle","bottom","left","iso_b_top","right_bottom_half"],
    "C": ["top","bottom","left"],
    "D": ["left","diag_d_top","diag_d_bottom"],
    "E": ["top","middle","bottom","left"],
    "F": ["top","middle","left"],
    "G": ["top","bottom","left","right_bottom"],
    "H": ["middle","left","right"],
    "I": ["top","bottom","center_vertical"],
    "J": ["bottom","right"],
    "K": ["left","diag_k_top","diag_r_leg"],
    "L": ["bottom","left"],
    "M": ["left","right","diag_m_right","diag_y_left"],
    "N": ["left","right","diagonal_zero"],
    "O": ["top","bottom","left","right"],
    "P": ["top","middle","left","right_top"],
    "Q": ["top","bottom","left","right","diag_w_right"],
    "R": ["top","middle","left","right_top_half","diag_r_leg"],
    "S": ["top","bottom","diagonal_zero"],
    "T": ["top","center_vertical"],
    "U": ["bottom","left","right"],
    "V": ["diag_v_right","diag_v_left"],
    "W": ["left","right","diag_w_left","diag_w_right"],
    "X": ["diagonal_z","diagonal_zero"],
    "Y": ["diag_y_left","diagonal_z"],
    "Z": ["top","bottom","diagonal_z"]
}

# ===============================
# GENERATE TEMPLATE ON-THE-FLY
# ===============================
def generate_template(char):
    """Generate template exactly as encoder draws it"""
    img_array = np.zeros((digit_height, digit_width), dtype=np.uint8)
    
    seg = segments.get(char, [])
    
    for y in range(digit_height):
        for x in range(digit_width):
            draw = False
            
            # Basic segments
            if "top" in seg and y < thickness:
                draw = True
            
            if "bottom" in seg and y > digit_height - thickness:
                draw = True
            
            if "middle" in seg and half_height - thickness < y < half_height + thickness:
                draw = True
            
            if "left" in seg and x < thickness:
                draw = True
            
            if "right" in seg and x > digit_width - thickness:
                draw = True
            
            if "left_top" in seg and x < thickness and y < half_height:
                draw = True
            
            if "left_bottom" in seg and x < thickness and y > half_height:
                draw = True
            
            if "right_top" in seg and x > digit_width - thickness and y < half_height:
                draw = True
            
            if "right_bottom" in seg and x > digit_width - thickness and y > half_height:
                draw = True
            
            if "center_vertical" in seg and digit_width//2 - thickness < x < digit_width//2 + thickness:
                draw = True
            
            if "right_bottom_half" in seg and x > digit_width - thickness and y > half_height:
                draw = True
            
            if "right_top_half" in seg and x > digit_width - thickness and y < half_height:
                draw = True
            
            # Diagonals
            if "diagonal_z" in seg:
                expected_x = digit_width - int((y * digit_width) / digit_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diagonal_zero" in seg:
                expected_x = int((y * digit_width) / digit_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_r_leg" in seg and y >= half_height:
                adjusted = y - half_height
                expected_x = int((adjusted * digit_width) / half_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_y_left" in seg and y <= half_height:
                expected_x = int((y * (digit_width // 2)) / half_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_m_right" in seg and y <= half_height:
                expected_x = digit_width - int((y * (digit_width // 2)) / half_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_k_top" in seg and y <= half_height:
                expected_x = digit_width - int((y * digit_width) / half_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_w_left" in seg and y >= half_height:
                adjusted = y - half_height
                expected_x = (digit_width // 2) - int((adjusted * (digit_width // 2)) / half_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_w_right" in seg and y >= half_height:
                adjusted = y - half_height
                expected_x = (digit_width // 2) + int((adjusted * (digit_width // 2)) / half_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_d_top" in seg and y <= half_height:
                expected_x = int((y * digit_width) / half_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_d_bottom" in seg and y >= half_height:
                adjusted = y - half_height
                expected_x = digit_width - int((adjusted * digit_width) / half_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_v_left" in seg:
                expected_x = int((y * (digit_width // 2)) / digit_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if "diag_v_right" in seg:
                expected_x = digit_width - int((y * (digit_width // 2)) / digit_height)
                if abs(x - expected_x) < thickness:
                    draw = True
            
            if draw:
                img_array[y, x] = 255
    
    return img_array

# ===============================
# COMPARISON
# ===============================
def compare_with_template(char_img, template):
    """Compare character with template (pixel-wise match)"""
    matches = np.sum(char_img == template)
    total_pixels = char_img.size
    return matches / total_pixels

# ===============================
# MATCH CHARACTER
# ===============================
def match_character(char_img, allowed_chars):
    """Find best matching character"""
    best_char = "?"
    best_score = 0.0
    
    for char in allowed_chars:
        template = generate_template(char)
        score = compare_with_template(char_img, template)
        
        if score > best_score:
            best_score = score
            best_char = char
    
    return best_char, best_score

# ===============================
# EXTRACT CODE
# ===============================
def extract_code(image_path):
    """Extract code from steganographic image"""
    
    # Load image
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    # Calculate positions
    total_width = TOTAL_CHARACTERS * digit_width + (TOTAL_CHARACTERS - 1) * spacing
    start_x = (width - total_width) // 2
    start_y = (height - digit_height) // 2
    
    extracted_code = ""
    
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    DIGITS = "0123456789"
    
    print("\nExtracting code...")
    print("-" * 60)
    
    # Process each character position
    for char_idx in range(10):
        # Determine channel and allowed characters
        if char_idx < 5:  # First 5: VANC2 (RED)
            channel_idx = 0
            allowed = LETTERS + DIGITS  # Can be letters or digits
            channel_name = "RED"
        elif char_idx < 9:  # Next 4: 0015 (BLUE)
            channel_idx = 2
            allowed = DIGITS
            channel_name = "BLUE"
        else:  # Last 1: V (GREEN)
            channel_idx = 1
            allowed = LETTERS
            channel_name = "GREEN"
        
        # Calculate character position
        x_offset = start_x + char_idx * (digit_width + spacing)
        
        # Extract character pixels from correct channel
        char_pixels = []
        for y in range(start_y, start_y + digit_height):
            row = []
            for x in range(x_offset, x_offset + digit_width):
                r, g, b = pixels[x, y]
                
                # Select correct channel
                if channel_idx == 0:
                    val = r
                elif channel_idx == 1:
                    val = g
                else:
                    val = b
                
                # Threshold
                row.append(255 if val > base_color else 0)
            char_pixels.append(row)
        
        # Convert to numpy
        char_img = np.array(char_pixels, dtype=np.uint8)
        
        # Match character
        detected_char, score = match_character(char_img, allowed)
        
        print(f"Position {char_idx} ({channel_name}): '{detected_char}' (confidence: {score:.1%})")
        
        extracted_code += detected_char
    
    return extracted_code


def extract_code_safe(image_path):
    """
    Extract code from steganographic image. Returns None on failure (file missing, invalid image).
    Use this when integrating with verify flow.
    """
    try:
        return extract_code(image_path)
    except (FileNotFoundError, OSError, Exception):
        return None


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    print("=" * 60)
    print("STEGANOGRAPHY CODE EXTRACTOR")
    print("=" * 60)

    import sys
    import glob
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        hidden_dir = os.path.join("generated", "hidden")
        candidates = glob.glob(os.path.join(hidden_dir, "*.png"))
        image_path = max(candidates, key=os.path.getmtime) if candidates else os.path.join(hidden_dir, "hidden_pan_format.png")
        print(f"Using latest: {image_path}\n")

    try:
        code = extract_code(image_path)

        print("\n" + "=" * 60)
        print(f"EXTRACTED CODE: {code}")
        print("=" * 60)

        if len(code) == 10 and "?" not in code:
            print("✓ VALID FORMAT (4 letters RED + 5 digits BLUE + 1 letter GREEN)")
            print(f"  RED:   {code[:4]}")
            print(f"  BLUE:  {code[4:9]}")
            print(f"  GREEN: {code[9]}")
        else:
            print("✗ Invalid length or low-confidence characters (?)")

    except FileNotFoundError:
        print(f"ERROR: {image_path} not found!")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()