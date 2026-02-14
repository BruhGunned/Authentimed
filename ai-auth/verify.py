import cv2
import json
import numpy as np
import os

TOLERANCES = {
    "blur": 0.7,
    "color": 80.0,
    "centroid": 12.0
}

def extract_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.Laplacian(gray, cv2.CV_64F).var()
    color = image.mean(axis=(0, 1))

    h, w = gray.shape
    roi = gray[int(0.15*h):int(0.45*h), int(0.05*w):int(0.6*w)]

    edges = cv2.Canny(roi, 100, 200)
    ys, xs = np.where(edges > 0)

    if len(xs) == 0:
        centroid = np.array([0, 0])
    else:
        centroid = np.array([xs.mean(), ys.mean()])

    return blur, color, centroid


# Load reference safely relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
reference_path = os.path.join(current_dir, "reference", "reference.json")

with open(reference_path) as f:
    ref = json.load(f)

ref_blur = ref["blur"]
ref_color = np.array(ref["color"])
ref_centroid = np.array(ref["centroid"])


def verify_packaging(scan_path, template_path):
    scan_img = cv2.imread(scan_path)
    template_img = cv2.imread(template_path)

    if scan_img is None or template_img is None:
        return False

    # Extract features from both
    scan_blur, scan_color, scan_centroid = extract_features(scan_img)
    ref_blur, ref_color, ref_centroid = extract_features(template_img)

    # Blur check
    if scan_blur < ref_blur * TOLERANCES["blur"]:
        return False

    # Color check
    if np.linalg.norm(scan_color - ref_color) > TOLERANCES["color"]:
        return False

    # Centroid check
    if np.linalg.norm(scan_centroid - ref_centroid) > TOLERANCES["centroid"]:
        return False

    return True
