"""
Reveal RGB channels from a PAN-format steganographic image into separate images.
"""
from PIL import Image
import os

THRESHOLD = 120


def reveal_channels(image_path, output_dir=None, prefix=""):
    """
    Split the hidden-code image into red, blue, and green channel reveal images.

    Args:
        image_path: Path to the steganographic image (e.g. from id_generation).
        output_dir: Directory for output images. If None, same directory as image_path.
        prefix: Optional prefix for output filenames (e.g. product_id) to avoid overwriting.

    Returns:
        dict: {"red": path, "blue": path, "green": path}
    """
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(image_path))

    os.makedirs(output_dir, exist_ok=True)

    red_img = Image.new("RGB", (width, height))
    blue_img = Image.new("RGB", (width, height))
    green_img = Image.new("RGB", (width, height))

    red_pixels = red_img.load()
    blue_pixels = blue_img.load()
    green_pixels = green_img.load()

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]

            if r > THRESHOLD:
                red_pixels[x, y] = (255, 255, 255)
            else:
                red_pixels[x, y] = (0, 0, 0)

            if b > THRESHOLD:
                blue_pixels[x, y] = (255, 255, 255)
            else:
                blue_pixels[x, y] = (0, 0, 0)

            if g > THRESHOLD:
                green_pixels[x, y] = (255, 255, 255)
            else:
                green_pixels[x, y] = (0, 0, 0)

    base = f"{prefix}_" if prefix else ""
    red_path = os.path.join(output_dir, f"{base}red_reveal.png")
    blue_path = os.path.join(output_dir, f"{base}blue_reveal.png")
    green_path = os.path.join(output_dir, f"{base}green_reveal.png")

    red_img.save(red_path)
    blue_img.save(blue_path)
    green_img.save(green_path)

    return {"red": red_path, "blue": blue_path, "green": green_path}


if __name__ == "__main__":
    import sys
    import glob
    from datetime import datetime
    if len(sys.argv) > 1:
        path = sys.argv[1]
        prefix = "standalone"
    else:
        hidden_dir = os.path.join("generated", "hidden")
        candidates = glob.glob(os.path.join(hidden_dir, "*.png"))
        if not candidates:
            path = os.path.join(hidden_dir, "hidden_pan_format.png")
            prefix = "standalone"
        else:
            path = max(candidates, key=os.path.getmtime)
            prefix = f"standalone_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Using: {path}")
    os.makedirs(os.path.join("generated", "reveals"), exist_ok=True)
    out = reveal_channels(path, output_dir=os.path.join("generated", "reveals"), prefix=prefix)
    # out = reveal_channels("test.jpeg", output_dir=os.path.join("generated", "reveals"), prefix=prefix)
    print("Reveal images created:", out)
