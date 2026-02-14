# Authentimed

AI + Blockchain Based Counterfeit Drug Detection System

## 🚀 Features

- QR Code Serialization
- AI Packaging Verification (OpenCV)
- Blockchain Registration (Ethereum Smart Contract)
- Replay Protection
- Full Stack Integration (Flask + React)

## 🛠 Tech Stack

- Flask
- React (Vite)
- Web3.py
- Solidity
- OpenCV

## 📦 How It Works

1. Manufacturer generates serialized QR
2. QR embedded into packaging
3. Product registered on blockchain
4. Consumer uploads packaging
5. AI verifies authenticity
6. QR extracted
7. Blockchain validates product
8. Final verdict returned

🚀 Deployment & Local Setup Guide
🧱 Project Structure
authentimed/
│
├── backend/                 # Flask + Web3 + OpenCV
├── frontend/                # React (Vite)
├── blockchain/              # Hardhat smart contract
└── README.md

🔥 Prerequisites

Make sure you have installed:

Node.js (LTS)

Python 3.10+

Git

npm

Hardhat (via npm)

🛠 1️⃣ Smart Contract Setup (Hardhat)
Step 1 — Navigate to Blockchain Folder
cd blockchain

Step 2 — Install Dependencies
npm install

Step 3 — Start Hardhat Local Node
npx hardhat node


You should see:

Started HTTP JSON-RPC server at http://127.0.0.1:8545


Keep this terminal running.

Step 4 — Deploy Smart Contract

Open a new terminal:

cd blockchain
npx hardhat run scripts/deploy.js --network localhost


You will see:

Contract deployed to: 0xABC123...


Copy this contract address.

🔗 2️⃣ Connect Backend to Smart Contract

Open:

backend/blockchain.py


Update:

contract_address = "PASTE_DEPLOYED_ADDRESS_HERE"


Make sure Web3 provider is:

Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

🧠 Important

Every time you restart the Hardhat node:

Blockchain state resets

Contract must be redeployed

Contract address must be updated in backend

🖥 3️⃣ Backend Setup (Flask + Web3 + OpenCV)
Step 1 — Navigate to Backend
cd backend

Step 2 — Create & Activate Virtual Environment (First Time Only)
python -m venv .venv
source .venv/bin/activate

Step 3 — Install Dependencies
pip install -r requirements.txt


If requirements.txt is not present:

pip install flask flask-cors web3 qrcode opencv-python

Step 4 — Run Backend
python app.py


You should see:

Running on http://127.0.0.1:5000


Backend is now live.

🌐 4️⃣ Frontend Setup (React + Vite)
Step 1 — Navigate to Frontend
cd frontend/authentimed-frontend

Step 2 — Install Node Modules
npm install

Step 3 — Start Dev Server
npm run dev


You should see:

http://localhost:5173


Open that in your browser.

🧪 5️⃣ Full System Startup Order

Always start services in this order:

Terminal 1 — Hardhat Node
cd blockchain
npx hardhat node

Terminal 2 — Deploy Contract
cd blockchain
npx hardhat run scripts/deploy.js --network localhost


Update contract address in backend.

Terminal 3 — Backend
cd backend
source .venv/bin/activate
python app.py

Terminal 4 — Frontend
cd frontend
npm run dev

