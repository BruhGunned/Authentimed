import cv2
import numpy as np
import json

def extract_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.Laplacian(gray, cv2.CV_64F).var()
    color = image.mean(axis=(0, 1))

    h, w = gray.shape
    roi = gray[int(0.15*h):int(0.45*h), int(0.05*w):int(0.6*w)]

    edges = cv2.Canny(roi, 100, 200)
    ys, xs = np.where(edges > 0)

    if len(xs) == 0:
        centroid = np.array([0.0, 0.0])
    else:
        centroid = np.array([xs.mean(), ys.mean()])

    return {
        "blur": float(blur),
        "color": color.tolist(),
        "centroid": centroid.tolist()
    }

img = cv2.imread("reference/real.png")
features = extract_features(img)

with open("reference/reference.json", "w") as f:
    json.dump(features, f, indent=2)

print("Reference model created")
