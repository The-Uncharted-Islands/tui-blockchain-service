from web3 import Web3, Account


block_server_port = 5009
bridge_server_port = 5109

block_server_apikey = ""

mainnet_provider = (
    ""
)
eth_provider = ""

merlin_provider = ""
bridge_contract_mainnet = ""

# chain_id = 1
chain_id = 421614


signer = Account.from_key(
    ""
)

weth_address = Web3.to_checksum_address("0x")
deposit_address = Web3.to_checksum_address("0x")
tui_address = Web3.to_checksum_address("0x")
stake_address = Web3.to_checksum_address("0x")
lp_address = Web3.to_checksum_address("0x")

dev_url = f""
prod_url = f""

dev_key = ""
prod_key = ""

API_URL = dev_url
API_KEY = dev_key

start_block = 36033570
scan_step = 1000
