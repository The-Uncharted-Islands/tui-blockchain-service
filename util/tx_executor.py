# -*- coding: utf-8 -*-
from web3 import Web3
import logging
import traceback


def try_execute_eip1559(call_data, extParams={}, account=None, client=None, chainId=1):
    try:
        execute_eip1559(
            call_data=call_data,
            extParams=extParams,
            account=account,
            client=client,
            chainId=chainId,
        )
    except Exception as e:
        logging.error(e)
        traceback.print_exception(e)


def execute_eip1559(call_data, extParams={}, account=None, client=None, chainId=1):
    # eip 1559
    latest_block = client.eth.get_block("latest")
    # Base fee in the latest block (in wei)
    base_fee_per_gas = latest_block.baseFeePerGas
    # Priority fee to include the transaction in the block
    max_priority_fee_per_gas = Web3.to_wei(1, "gwei")
    # max_priority_fee_per_gas = Web3.to_wei(0.000000003, 'gwei')
    # Maximum amount you’re willing to pay
    max_fee_per_gas = (2 * base_fee_per_gas) + max_priority_fee_per_gas
    # max_fee_per_gas = base_fee_per_gas + max_priority_fee_per_gas

    base_params = {
        "type": "0x2",
        "value": 0,
        "from": account.address,
        "nonce": client.eth.get_transaction_count(account.address),
        "maxFeePerGas": max_fee_per_gas,
        "maxPriorityFeePerGas": max_priority_fee_per_gas,
        "chainId": chainId,
    }

    params = {}
    params.update(base_params)
    params.update(extParams)

    transaction = call_data.build_transaction(params)

    # gas = client.eth.estimateGas(transaction)
    # print(gas)
    signed_txn = account.sign_transaction(transaction)
    # tx_hash = Web3.to_hex(client.keccak(signed_txn.rawTransaction))
    # logging.info(f"Transaction Hash = {tx_hash}")

    tx_hash = client.eth.send_raw_transaction(signed_txn.rawTransaction)

    transaction_receipt = client.eth.wait_for_transaction_receipt(tx_hash)

    if transaction_receipt.status:
        print("Transaction successful! hash:", tx_hash.hex())
        # print(f"Explorer link: {explorer_link}{tx_hash.hex()}")
    else:
        print("Transaction failed! hash:", tx_hash.hex())
    return tx_hash


def estimate_gas(call_data, extParams={}, account=None, client=None, chainId=1):

    # eip 1559
    latest_block = client.eth.get_block("latest")
    # Base fee in the latest block (in wei)
    base_fee_per_gas = latest_block.baseFeePerGas
    # Priority fee to include the transaction in the block
    max_priority_fee_per_gas = Web3.to_wei(1, "gwei")
    # max_priority_fee_per_gas = Web3.to_wei(0.000000003, 'gwei')
    # Maximum amount you’re willing to pay
    max_fee_per_gas = (2 * base_fee_per_gas) + max_priority_fee_per_gas
    # max_fee_per_gas = base_fee_per_gas + max_priority_fee_per_gas

    base_params = {
        "type": "0x2",
        "value": 0,
        "from": account.address,
        "nonce": client.eth.get_transaction_count(account.address),
        "maxFeePerGas": max_fee_per_gas,
        "maxPriorityFeePerGas": max_priority_fee_per_gas,
        "chainId": chainId,
    }

    params = {}
    params.update(base_params)
    params.update(extParams)

    transaction = call_data.build_transaction(params)

    gas = client.eth.estimate_gas(transaction)
    return gas


def executeV1(call_data, extParams={}, account=None, client=None, chainId=1):

    gas = 30000000  
    gas_price = Web3.to_wei(1, "gwei")

    base_params = {
        "gas": gas,
        "gasPrice": gas_price,
        "value": 0,
        "from": account.address,
        "nonce": client.eth.get_transaction_count(account.address),
        "chainId": chainId,
    }

    params = {}
    params.update(base_params)
    params.update(extParams)

    transaction = call_data.build_transaction(params)

    signed_txn = account.sign_transaction(transaction)

    tx_hash = client.eth.send_raw_transaction(signed_txn.rawTransaction)

    transaction_receipt = client.eth.wait_for_transaction_receipt(tx_hash)

    if transaction_receipt.status:
        print("Transaction successful! hash:", tx_hash.hex())
    else:
        print("Transaction failed! hash:", tx_hash.hex())
    return tx_hash


def transferETH(to_address, amount, account=None, client=None):
    latest_block = client.eth.get_block("latest")
    # Base fee in the latest block (in wei)
    base_fee_per_gas = latest_block.baseFeePerGas
    # Priority fee to include the transaction in the block
    max_priority_fee_per_gas = Web3.to_wei(1, "gwei")
    # Maximum amount you’re willing to pay
    max_fee_per_gas = (2 * base_fee_per_gas) + max_priority_fee_per_gas

    value = client.to_wei(amount, "ether")
    params = {
        "gas": 21000,
        "type": "0x2",
        "from": account.address,
        "to": to_address,
        "value": value,
        "nonce": client.eth.get_transaction_count(account.address),
        "maxFeePerGas": max_fee_per_gas,  # Maximum amount you’re willing to pay
        "maxPriorityFeePerGas": max_priority_fee_per_gas,  # Priority fee to include the transaction in the block
        "chainId": 1,
    }
    signTx = account.sign_transaction(params)
    logging.info(f"from {account.address} to {to_address} value {value}")
    tx_hash = client.eth.send_raw_transaction(signTx.rawTransaction)
    transaction_receipt = client.eth.wait_for_transaction_receipt(tx_hash)

    if transaction_receipt.status:
        print("Transaction successful! hash:", tx_hash.hex())
    else:
        print("Transaction failed! hash:", tx_hash.hex())
    return tx_hash
