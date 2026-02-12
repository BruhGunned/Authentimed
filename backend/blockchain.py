from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#UPDATE CONTRACT ADDRESS HERE

contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"


with open("abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

account = w3.eth.accounts[0]

def register_product(product_id):
    tx_hash = contract.functions.registerProduct(product_id).transact({
        'from': account
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)

def verify_product(product_id):
    result = contract.functions.verifyProduct(product_id).call({
        'from': account
    })

    tx_hash = contract.functions.verifyProduct(product_id).transact({
        'from': account
    })

    w3.eth.wait_for_transaction_receipt(tx_hash)

    return result

