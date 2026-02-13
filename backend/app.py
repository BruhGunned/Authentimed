from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import qrcode

import psycopg2
from db import init_db
from qr_overlay import replace_qr
from qr_extractor import extract_qr_data
from ai_verifier import verify_packaging
from blockchain import verify_product, register_product
from id_generation import generate_hidden_code_image
from extractor import extract_code_safe

# ------------------------------
# App Setup
# ------------------------------

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
QR_FOLDER = "qr_codes"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# Init DB when possible (for code_generator). App still runs if PostgreSQL is down.
try:
    init_db()
except psycopg2.OperationalError:
    pass  # DB not available; /generate will return 503 until PostgreSQL is running


# ------------------------------
# Health Check Route
# ------------------------------

@app.route("/", methods=["GET"])
def home():
    return "Authentimed Backend Running"


# ------------------------------
# Manufacturer Endpoint
# ------------------------------

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # 1️⃣ Unique product ID (DB-backed, format: 4 letters + 5 digits + 1 letter)
        temp_hidden = os.path.join(QR_FOLDER, "_temp_hidden.png")
        product_id, hidden_path = generate_hidden_code_image(
            code=None,
            output_path=temp_hidden,
            database_url=None,
        )
        final_hidden = os.path.join(QR_FOLDER, f"{product_id}_hidden.png")
        if hidden_path != final_hidden and os.path.exists(hidden_path):
            os.rename(hidden_path, final_hidden)
            hidden_path = final_hidden

        # 2️⃣ Generate QR Code (same ID)
        qr_path = os.path.join(QR_FOLDER, f"{product_id}.png")
        img = qrcode.make(product_id)
        img.save(qr_path)

        # 3️⃣ Embed QR into packaging
        base_package = "../ai-auth/reference/real.png"
        output_package = os.path.join(QR_FOLDER, f"{product_id}_packaged.png")
        replace_qr(base_package, qr_path, output_package)

        # 4️⃣ Register on Blockchain
        register_product(product_id)

        return jsonify({
            "Status": "QR Generated, Embedded & Registered",
            "Product ID": product_id,
            "Packaged Image": output_package,
            "Hidden Code Image": hidden_path,
        }), 200

    except psycopg2.OperationalError as e:
        return jsonify({
            "error": "Database unavailable. Start PostgreSQL or set DATABASE_URL.",
            "detail": str(e)
        }), 503
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ------------------------------
# Consumer Endpoint
# ------------------------------

@app.route("/verify", methods=["POST"])
def verify():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 🔹 AI Verification
        ai_passed = verify_packaging(filepath)

        if not ai_passed:
            return jsonify({
                "AI Result": "FAIL",
                "Blockchain Result": "SKIPPED",
                "Final Verdict": "COUNTERFEIT"
            }), 200

        # 🔹 Extract product ID: try QR first, then steganographic hidden code
        product_id = extract_qr_data(filepath)
        if not product_id:
            product_id = extract_code_safe(filepath)
        if product_id and "?" in product_id:
            product_id = None

        if not product_id:
            return jsonify({
                "AI Result": "PASS",
                "Blockchain Result": "CODE NOT FOUND",
                "Final Verdict": "COUNTERFEIT"
            }), 200

        # 🔹 Blockchain Verification
        blockchain_valid = verify_product(product_id)

        if blockchain_valid:
            return jsonify({
                "AI Result": "PASS",
                "Blockchain Result": "VALID",
                "Final Verdict": "GENUINE",
                "Product ID": product_id
            }), 200
        else:
            return jsonify({
                "AI Result": "PASS",
                "Blockchain Result": "REPLAYED OR INVALID",
                "Final Verdict": "COUNTERFEIT",
                "Product ID": product_id
            }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ------------------------------
# Run Server
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)
