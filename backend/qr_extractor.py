import cv2
from pyzbar.pyzbar import decode

def extract_qr_data(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    qr_codes = decode(img)

    if not qr_codes:
        return None

    return qr_codes[0].data.decode("utf-8")
