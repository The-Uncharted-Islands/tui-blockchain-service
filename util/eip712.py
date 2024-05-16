from eth_account import Account
from web3 import Web3
from eth_account.messages import encode_structured_data, encode_typed_data, encode_defunct
import logging

def sign_message(signer: Account, nonce, to, chainId, contract_address):
    message = Web3.solidity_keccak(['address', 'address', 'uint256', 'uint256'], 
                                   [contract_address, to, nonce, chainId])
    signed = signer.sign_message(encode_defunct(message))
    return signed.v, signed.r, signed.s


def sign_eip712_message(signer: Account, nonce, to, chainId, contract_address):
    
    domain = {
        "name": "EIP712Storage",
        "version": "1",
        "chainId": chainId,
        "verifyingContract": contract_address,
    }

    value = {
        "nonce": nonce,
        "to": to,
    }

    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"}
            ],
            'Mint': [
                { 'name': 'nonce', 'type': 'uint256' },
                { 'name': 'to', 'type': 'address' },
            ]
        },
        "domain": domain,
        "primaryType": 'Mint',
        "message": value
    }

    encoded_data = encode_structured_data(primitive=typed_data)
    # encoded_data = encode_typed_data(typed_data)
    
    # signer.sign_typed_data(encoded_data)
    signed = signer.sign_message(encoded_data)
    print(signed)

    recover_address = Account.recover_message(encoded_data, signature=signed.signature)
    assert signer.address == recover_address
    logging.info(f"signer.address {signer.address} recover {recover_address} to address {to}")

    return signed.signature

    # return signed['signature']
    


