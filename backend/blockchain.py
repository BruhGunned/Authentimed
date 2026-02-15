from web3 import Web3
import json
import os
from web3.exceptions import ContractLogicError

# ==============================
# 🔷 Connect to Sepolia
# ==============================
import os
from dotenv import load_dotenv

load_dotenv()

SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")


w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))

# Your deployed contract address (Sepolia)
contract_address = Web3.to_checksum_address("0xc9d80E54970558025ACE45c0751E039A533777c6")

with open("abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

# Derive account from private key
account = w3.eth.account.from_key(PRIVATE_KEY)


# ==============================
# 🔷 Helpers
# ==============================

def is_node_connected():
    return w3.is_connected()


def safe_transact(function_call):
    try:
        nonce = w3.eth.get_transaction_count(account.address)

        # Aggressive gas settings (fast confirmation)
        max_fee = w3.to_wei(40, "gwei")        # total max fee
        priority_fee = w3.to_wei(5, "gwei")    # miner tip

        tx = function_call.build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gas": 300000,
            "maxFeePerGas": max_fee,
            "maxPriorityFeePerGas": priority_fee,
            "chainId": 11155111  # Sepolia chain ID
        })

        signed_tx = account.sign_transaction(tx)

        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return {"success": True, "receipt": receipt}

    except ContractLogicError as e:
        return {"success": False, "error": f"Contract revert: {str(e)}"}

    except Exception as e:
        return {"success": False, "error": str(e)}



# ==============================
# 🔷 Contract Functions
# ==============================

def register_product(product_id):
    return safe_transact(
        contract.functions.registerProduct(product_id)
    )


def verify_product(product_id):
    return safe_transact(
        contract.functions.verifyProduct(product_id)
    )


def get_product_state(product_id):
    return contract.functions.getProductState(product_id).call()


def get_manufacturer(product_id):
    return contract.functions.getManufacturer(product_id).call()

