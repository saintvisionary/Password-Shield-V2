from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

def log_to_blockchain(hash_type, hash_value, result):
    """Log the hash result to the blockchain for immutability."""
    transaction = {
        'to': '0xRecipientAddress',  # Replace with the recipient's address
        'from': w3.eth.accounts[0],
        'value': w3.toWei(0.001, 'ether'),  # Small transaction value
        'data': w3.toHex(text=f"{hash_type}:{hash_value}:{result}")
    }
    signed_txn = w3.eth.account.signTransaction(transaction, private_key='YourPrivateKey')  # Replace with your private key
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return w3.toHex(tx_hash)
