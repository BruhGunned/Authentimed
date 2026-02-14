import cv2
import numpy as np

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


def verify_packaging(scan_path, template_path):
    scan_img = cv2.imread(scan_path)
    template_img = cv2.imread(template_path)

    if scan_img is None or template_img is None:
        return False

    scan_blur, scan_color, scan_centroid = extract_features(scan_img)
    template_blur, template_color, template_centroid = extract_features(template_img)

    # Blur check
    if scan_blur < template_blur * TOLERANCES["blur"]:
        return False

    # Color check
    if np.linalg.norm(scan_color - template_color) > TOLERANCES["color"]:
        return False

    # Centroid check
    if np.linalg.norm(scan_centroid - template_centroid) > TOLERANCES["centroid"]:
        return False

    return True
