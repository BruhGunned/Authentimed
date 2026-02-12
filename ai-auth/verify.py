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


def verify_packaging(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return False

    blur, color, centroid = extract_features(img)

    if blur < ref_blur * TOLERANCES["blur"]:
        return False

    if np.linalg.norm(color - ref_color) > TOLERANCES["color"]:
        return False

    if np.linalg.norm(centroid - ref_centroid) > TOLERANCES["centroid"]:
        return False

    return True
