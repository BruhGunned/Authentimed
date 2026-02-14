from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import qrcode
import hashlib
import re
from web3 import Web3

from qr_overlay import replace_qr
from qr_extractor import extract_qr_data
from ai_verifier import verify_packaging

from blockchain import (
    w3,contract,
    vote_manufacturer,
    register_template_hash,
    register_product,
    verify_product,
    get_manufacturer,
    is_manufacturer_approved
)


from db import init_db, record_scan, get_scan_info





# =====================================================
# 🔷 Utility
# =====================================================

def is_valid_product_id(product_id):
    pattern = r"^MEDICINEX-[a-f0-9]{8}$"
    return re.match(pattern, product_id) is not None


# =====================================================
# 🔷 App Setup
# =====================================================

app = Flask(__name__)
CORS(app)


init_db()

UPLOAD_FOLDER = "uploads"
QR_FOLDER = "qr_codes"
TEMPLATE_FOLDER = "templates"
TEMP_FOLDER = "temp"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)


# =====================================================
# 🔷 Health Check
# =====================================================

@app.route("/", methods=["GET"])
def home():
    return "Authentimed Backend Running"


# =====================================================
# 🔷 MANUFACTURER ROUTES
# =====================================================

@app.route("/manufacturer/onboard", methods=["POST"])
def onboard_manufacturer():
    try:
        manufacturer = request.form.get("account")

        if not manufacturer:
            return jsonify({"error": "Manufacturer account required"}), 400

        vote_manufacturer(manufacturer)

        if not is_manufacturer_approved(manufacturer):
            return jsonify({"error": "Manufacturer approval failed"}), 400

        if "file" not in request.files:
            return jsonify({"error": "No template uploaded"}), 400

        file = request.files["file"]
        template_path = f"{TEMPLATE_FOLDER}/{manufacturer}.png"
        file.save(template_path)

        with open(template_path, "rb") as f:
            hash_hex = hashlib.sha256(f.read()).hexdigest()

        hash_bytes = Web3.to_bytes(hexstr=hash_hex)
        register_template_hash(hash_bytes, manufacturer)

        return jsonify({
            "Status": "Manufacturer Approved & Template Registered"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/manufacturer/generate", methods=["POST"])
def generate_product():
    try:
        manufacturer = request.form.get("account")

        if not manufacturer:
            return jsonify({"error": "Manufacturer account required"}), 400

        template_path = f"{TEMPLATE_FOLDER}/{manufacturer}.png"

        if not os.path.exists(template_path):
            return jsonify({"error": "Template not registered"}), 400

        product_id = f"MEDICINEX-{uuid.uuid4().hex[:8]}"

        qr_path = f"{QR_FOLDER}/{product_id}.png"
        img = qrcode.make(product_id)
        img.save(qr_path)

        output_path = f"{QR_FOLDER}/{product_id}_packaged.png"
        replace_qr(template_path, qr_path, output_path)

        tx_result = register_product(product_id, manufacturer)

        if not tx_result["success"]:
            return jsonify({"error": tx_result["error"]}), 400

        return jsonify({
            "Product ID": product_id,
            "Manufacturer ID": manufacturer,
            "Status": "Registered"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



# =====================================================
# 🔷 INTERNAL VERIFICATION LOGIC
# =====================================================
def handle_verification(role):
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        scan_path = f"{TEMP_FOLDER}/{file.filename}"
        file.save(scan_path)

        # 🔹 Extract QR
        product_id = extract_qr_data(scan_path)

        if not product_id or not is_valid_product_id(product_id):
            os.remove(scan_path)
            return jsonify({
                "Final Verdict": "COUNTERFEIT",
                "Reason": "Invalid or Missing QR"
            }), 200

        # 🔹 Check manufacturer exists
        manufacturer = get_manufacturer(product_id)

        if manufacturer == "0x0000000000000000000000000000000000000000":
            os.remove(scan_path)
            return jsonify({
                "Final Verdict": "COUNTERFEIT",
                "Reason": "Not Registered on Blockchain"
            }), 200

        # 🔹 AI Packaging Check
        template_path = f"{TEMPLATE_FOLDER}/{manufacturer}.png"
        ai_pass = verify_packaging(scan_path, template_path)

        os.remove(scan_path)

        if not ai_pass:
            return jsonify({
                "Final Verdict": "COUNTERFEIT",
                "Reason": "Packaging Tampered"
            }), 200

        # 🔹 Get blockchain state
        state = contract.functions.getProductState(product_id).call()

        # Enum mapping:
        # 0 = NONE
        # 1 = VALID
        # 2 = REPLAYED

        # ==============================
        # 🔥 Pharmacist (Transactional)
        # ==============================
        if role == "pharmacist":

            if state == 1:  # VALID → First Scan
                pharmacist_account = w3.eth.accounts[4]
                verify_product(product_id, pharmacist_account)

                record_scan(product_id)

                return jsonify({
                    "Final Verdict": "GENUINE",
                    "Scan Status": "First Pharmacist Scan",
                    "Product ID": product_id
                }), 200

            if state == 2:  # Already REPLAYED
                return jsonify({
                    "Final Verdict": "COUNTERFEIT",
                    "Reason": "Replay Detected",
                    "Product ID": product_id
                }), 200

            return jsonify({
                "Final Verdict": "COUNTERFEIT"
            }), 200

        # ==============================
        # 🔥 Consumer (Read-Only)
        # ==============================
        if role == "consumer":

            if state == 1:
                return jsonify({
                    "Final Verdict": "UNVERIFIED",
                    "Message": "Never scanned by pharmacist",
                    "Product ID": product_id
                }), 200

            if state == 2:
                scan_info = get_scan_info(product_id)

                return jsonify({
                    "Final Verdict": "VERIFIED",
                    "Product ID": product_id,
                    "First Scan Time": scan_info["first_scan_time"] if scan_info else "Unknown"
                }), 200

            return jsonify({
                "Final Verdict": "COUNTERFEIT"
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# =====================================================
# 🔷 PHARMACIST ROUTE
# =====================================================

@app.route("/pharmacist/verify", methods=["POST"])
def pharmacist_verify():
    return handle_verification("pharmacist")


# =====================================================
# 🔷 CONSUMER ROUTE
# =====================================================

@app.route("/consumer/verify", methods=["POST"])
def consumer_verify():
    return handle_verification("consumer")


# =====================================================
# 🔷 Serve QR Images
# =====================================================

@app.route("/qr_codes/<path:filename>")
def serve_qr(filename):
    return send_from_directory(QR_FOLDER, filename)


# =====================================================
# 🔷 Run
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)



@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        "error": "Internal server error",
        "details": str(e)
    }), 500

