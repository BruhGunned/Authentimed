"""
Test runner for steganography flow.

Usage:
  - With any argument: uses `test.jpeg` (project root or generated/hidden)
  - Without arguments: generates a hidden image via `id_generation`.

Flow:
  stego image -> revealer.reveal_channels -> extractor.extract_code
"""
import sys
import os
from datetime import datetime


def find_test_file():
    candidates = [
        os.path.join(os.getcwd(), "test.jpeg"),
        os.path.join(os.getcwd(), "generated", "hidden", "test.jpeg"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def main():
    # Decide flow
    if len(sys.argv) > 1:
        print("Argument detected — attempting test.jpeg flow")
        stego = find_test_file()
        if not stego:
            print("ERROR: test.jpeg not found in project root or generated/hidden")
            sys.exit(2)
        prefix = f"testfile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    else:
        print("No argument — generating hidden PAN image via id_generation")
        from id_generation import generate_hidden_code_image
        code, stego = generate_hidden_code_image()
        print(f"Generated stego image: {stego} (code: {code})")
        prefix = code

    # Reveal channels
    from revealer import reveal_channels
    reveals_dir = os.path.join("generated", "reveals")
    os.makedirs(reveals_dir, exist_ok=True)
    print(f"Revealing channels for: {stego}")
    out = reveal_channels(stego, output_dir=reveals_dir, prefix=prefix)
    print("Reveal outputs:", out)

    # Extract code from original stego image
    from extractor import extract_code
    print(f"Extracting code from: {stego}")
    try:
        code = extract_code(stego)
        print("Extracted code:", code)
    except FileNotFoundError:
        print(f"ERROR: stego file not found: {stego}")
    except Exception as e:
        print("ERROR during extraction:", e)


if __name__ == "__main__":
    main()
