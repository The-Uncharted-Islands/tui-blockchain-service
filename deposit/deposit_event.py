from web3 import Web3
import datetime
from util.logger import logger
import requests
import json
import util.signal_handler as signal_handler
import os
import traceback
from setting import (
    mainnet_provider,
    start_block,
    scan_step,
    API_URL,
    API_KEY,
    deposit_address,
    tui_address,
)


transfer_event = "Transfer"
client = Web3(Web3.HTTPProvider(mainnet_provider))
deposit_data_file = "file/deposit-data.json"

transfer_config_data = {}

with open("file/tui.abi.json") as f:
    tui_abi = json.load(f)
    tui_contract = client.eth.contract(address=tui_address, abi=tui_abi)


def try_get_latest_block():
    try:
        latest_block = client.eth.get_block("latest")
        latest_block_number = latest_block["number"]
        return latest_block_number
    except Exception as e:
        traceback.print_exc()
        logger.info("get latest block exception")
    return -1


def on_transfer_event(event):

    logger.info(event)

    amount = event.args["value"]
    from_ = event.args["from"]
    to = event.args["to"]
    hash = event["transactionHash"].hex()
    blockTime = event["blockNumber"]

    tos = Web3.to_checksum_address(to)
    if tos != deposit_address:
        return

    logger.info(
        f"transfer event from {from_} to {to} amount {amount} hash {hash} blockTime {blockTime}"
    )

    amount2 = Web3.from_wei(amount, "ether")
    post_data = {
        "address": from_,
        "itemId": 1,
        "amount": int(amount2),
        "apiKey": API_KEY,
        "txHash": hash,
        "blockTime": blockTime,
    }

    response = requests.post(API_URL, json=post_data)
    print(response.text)


def load_config():

    global transfer_config_data
    if not os.path.isfile(deposit_data_file):
        transfer_config_data = {
            "block": start_block,
        }
    else:
        with open(deposit_data_file, "r") as f:
            transfer_config_data = json.load(f)


def fetch_contract_events():

    to_Block = transfer_config_data["block"]

    latest_block_number = try_get_latest_block()
    if latest_block_number == -1:
        # logger.info("get latest block error")
        return

    # to last block
    while signal_handler.is_running():

        from_block = to_Block + 1
        to_Block = from_block + scan_step

        if from_block > latest_block_number:
            logger.info("scan log end")
            break

        if to_Block >= latest_block_number:
            to_Block = latest_block_number

        event_count = 0
        event_log = tui_contract.events[transfer_event]().get_logs(
            fromBlock=from_block,
            toBlock=to_Block,
        )

        transfer_config_data["block"] = to_Block

        for event in event_log:
            on_transfer_event(event)
        event_count = event_count + len(event_log)

        # save
        with open(deposit_data_file, "w") as file_object:
            data = json.dumps(transfer_config_data)
            file_object.write(data)

        logger.info(f"fetch event log {from_block} - {to_Block} count {event_count}")


def _once_scan():

    logger.info("scan asset pool events")
    try:
        fetch_contract_events()
    except Exception as e:
        traceback.print_exc()
        logger.info("fetch events error")


def once_load_scan():
    load_config()
    _once_scan()
