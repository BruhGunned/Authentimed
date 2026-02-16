# AuthentiMED

### AI + Blockchain Pharmaceutical Authentication System

AuthentiMED is a full-stack Web3 pharmaceutical authentication system that combines:

* AI-powered packaging verification
* Blockchain-backed product registration
* QR + hidden strip dual-factor linking
* Role-based verification flows (Manufacturer / Pharmacist / Consumer)

It prevents counterfeit medicine circulation using immutable on-chain logs and image-based validation.

---

## 🚀 Architecture Overview

```
Manufacturer → Registers batch on-chain
           ↓
Blockchain (Sepolia / Hardhat)
           ↓
Pharmacist → First verification + activation
           ↓
Consumer → Final authenticity check
```

Core Layers:

* **Frontend** – React (Vite)
* **Backend** – Flask (REST API)
* **Blockchain** – Solidity + Hardhat (Sepolia)
* **Database** – PostgreSQL (Supabase)
* **AI Layer** – Packaging + hidden strip verification

---

# 🧠 Role Workflows

## 1️⃣ Manufacturer

* Upload packaging template
* System:

  * Generates QR
  * Embeds hidden strip code
  * Registers Product ID on-chain
* Returns:

  * Product ID
  * Blockchain status
  * Generated packaging image

Endpoint:

```
POST /manufacturer/generate
```

---

## 2️⃣ Pharmacist

* Upload image (full pack / QR / strip)
* System:

  * Extracts QR
  * Checks on-chain record
  * Verifies packaging integrity
  * Activates product (first scan recorded)

Endpoint:

```
POST /pharmacist/verify
```

---

## 3️⃣ Consumer

* Upload image
* System:

  * Validates QR / strip
  * Checks first scan status
  * Flags replay attempts
  * Displays scan history

Endpoint:

```
POST /consumer/verify
```

---

# 🛠 Tech Stack

## Frontend

* React (Vite)
* React Router
* HTML-CSS-JAVASCRIPT

## Backend

* Flask
* REST APIs
* QR extraction
* Image processing
* AI verification module
* PostgreSQL (Supabase)

## Blockchain

* Solidity smart contract
* Hardhat
* Sepolia testnet
* Web3.py
* Ethers-compatible

---

# 📂 Project Structure

```
authentimed/
│
├── backend/                # Flask backend
│   ├── app.py
│   ├── ai_verifier.py
│   ├── qr_extractor.py
│   └── ...
│
├── blockchain/             # Hardhat project
│   ├── contracts/
│   ├── scripts/
│   └── hardhat.config.js
│
├── frontend/               # Stable UI
├── frontend2/              # UI redesign branch work
│
├── requirements.txt
└── README.md
```

---

# 🔧 Setup Instructions

## 1️⃣ Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
pip install -r ../requirements.txt
python app.py
```

Runs at:

```
http://127.0.0.1:5000
```

---

## 2️⃣ Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at:

```
http://localhost:5173
```

---

## 3️⃣ Blockchain

```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
```

---

# 🔐 Security Features

* Immutable product registration
* QR + strip dual-factor linking
* Replay attack detection
* First-scan timestamp recording
* AI packaging tamper detection
* Role-based verification flow
* On-chain identity validation

---

# ⚠ Known Limitations

* Sepolia gas latency
* No Layer-2 scaling yet
* Single-node Flask deployment
* No production-grade CDN/storage

---

# 🌱 Future Improvements

* Layer-2 deployment (Polygon / Arbitrum)
* IPFS storage for packaging
* Zero-knowledge verification
* Wallet-based manufacturer authentication
* Multi-scan anomaly analytics
* Production Docker deployment

---




