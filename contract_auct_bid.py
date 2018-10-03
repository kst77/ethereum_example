import time
from web3 import Web3, HTTPProvider
import contract_auct_abi

# Links
# https://hackernoon.com/ethereum-smart-contracts-in-python-a-comprehensive-ish-guide-771b03990988

# https://web3py.readthedocs.io/en/stable/contracts.html
# https://remix.ethereum.org
# https://infura.io/
# https://faucet.metamask.io/
# https://ropsten.etherscan.io/address/0x332804ecfc4f6741073c0c849da8047702f0779a

contract_address     = '0xE051B4D836f28b637CEA8923c153Bd5654F82290'


wallet_private_key   = '4605d613195a34168a3888dee81ea3a8a2b272b7efc5c858e801349b2a2611af'
wallet_address       = '0x08f69300323531c6bA0619A2c6892F4FC9482740'


'''
wallet_private_key   = '9ba77b1f502a9b917b615e28d93de166bfdce2fd3c273d808b65804f96ce6af7'
wallet_address       = '0x2E2fa3602696bd889EeD12C4af13d22Cc9E8CC55'
'''


w3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/476c3b6c9d274aa2af7088784c281d52'))
w3.eth.enable_unaudited_features()

itemId = 1
tokencount = 1
amount_in_wei = w3.toWei(0.1,'ether')


contract = w3.eth.contract(address = contract_address, abi = contract_auct_abi.abi)
nonce = w3.eth.getTransactionCount(wallet_address)

def sendtran(txn):
    signed_txn = w3.eth.account.signTransaction(txn, private_key=wallet_private_key)
    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.getTransactionReceipt(result)

    while tx_receipt is None:
        time.sleep(10)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        print(tx_receipt)


txn_dict = contract.functions.bid(itemId, tokencount).buildTransaction({
    'chainId': 3,
    'gas': 2000000, #gas_estimate = contract.functions.fillitems(4).estimateGas()
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce,
    'value': amount_in_wei
})

sendtran(txn_dict)



