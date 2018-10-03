import time
from web3 import Web3, HTTPProvider
import contract_auct_abi

contract_address     = '0xE051B4D836f28b637CEA8923c153Bd5654F82290'

w3 = Web3(Web3.WebsocketProvider("wss://ropsten.infura.io/ws"))

contract = w3.eth.contract(address = contract_address, abi = contract_auct_abi.abi)


def handle_event(event):
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = contract.events.BidEvent().processReceipt(receipt)
    print("Bid from {} for item {} in {} , balance {}".format(result[0].args.addr, result[0].args.itemId, result[0].args.count, result[0].args.balance))

def log_loop(event_filter):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(2)

block_filter = w3.eth.filter({'fromBlock':'latest', 'address': contract_address})
log_loop(block_filter)