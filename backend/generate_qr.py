import qrcode
import os

QR_FOLDER = "qr_codes"
os.makedirs(QR_FOLDER, exist_ok=True)

for i in range(1, 6):
    product_id = f"MEDICINEX-{i:04d}"
    img = qrcode.make(product_id)
    img.save(os.path.join(QR_FOLDER, f"{product_id}.png"))
