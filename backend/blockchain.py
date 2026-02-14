from web3 import Web3
import json
import hashlib
from web3.exceptions import ContractLogicError
from requests.exceptions import ConnectionError





w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

with open("abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

# Hardhat default accounts
validators = [
    w3.eth.accounts[0],
    w3.eth.accounts[1],
    w3.eth.accounts[2]
]

def is_node_connected():
    return w3.is_connected()
def is_valid_address(address):
    return Web3.is_address(address)
def safe_transact(function_call, sender):
    try:
        tx = function_call.transact({"from": sender})
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        return {"success": True, "receipt": receipt}
    except ContractLogicError as e:
        return {"success": False, "error": f"Contract revert: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}



def vote_manufacturer(candidate):
    if not is_valid_address(candidate):
        return {"success": False, "error": "Invalid Ethereum address"}

    if not is_node_connected():
        return {"success": False, "error": "Blockchain node not connected"}

    for validator in validators:
        result = safe_transact(
            contract.functions.voteManufacturer(candidate),
            validator
        )
        if not result["success"]:
            return result

    return {"success": True}

def is_contract_deployed():
    code = w3.eth.get_code(contract_address)
    return code != b''



def register_template_hash(hash_bytes, manufacturer):
    return safe_transact(
        contract.functions.registerTemplateHash(hash_bytes),
        manufacturer
    )


def register_product(product_id, manufacturer):
    if not is_valid_address(manufacturer):
        return {"success": False, "error": "Invalid Ethereum address"}

    return safe_transact(
        contract.functions.registerProduct(product_id),
        manufacturer
    )


def verify_product(product_id, sender):
    return safe_transact(
        contract.functions.verifyProduct(product_id),
        sender
    )

def get_manufacturer(product_id):
    return contract.functions.getManufacturer(product_id).call()

def is_manufacturer_approved(manufacturer):
    return contract.functions.approvedManufacturers(manufacturer).call()





