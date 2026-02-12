import cv2

# Ratios based on original 720x405 template
QR_SIZE_RATIO = 115 / 720
QR_X_RATIO = 577 / 720
QR_Y_RATIO = 170 / 405

def replace_qr(package_image_path, new_qr_path, output_path):
    package = cv2.imread(package_image_path)
    new_qr = cv2.imread(new_qr_path)

    if package is None or new_qr is None:
        return False

    h, w, _ = package.shape

    # Compute relative QR size
    qr_size = int(w * QR_SIZE_RATIO)
    new_qr = cv2.resize(new_qr, (qr_size, qr_size))

    # Compute relative position
    x_start = int(w * QR_X_RATIO)
    y_start = int(h * QR_Y_RATIO)

    package[y_start:y_start+qr_size, x_start:x_start+qr_size] = new_qr

    cv2.imwrite(output_path, package)

    return True
