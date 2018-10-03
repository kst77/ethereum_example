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
wallet_private_key   = 'b540ca1f4aef7b994dfa0233f800c50c3f9640f435e4a8ecf7ac8811b954684f'
wallet_address       = '0x332804eCFc4F6741073c0c849DA8047702F0779A'

w3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/476c3b6c9d274aa2af7088784c281d52'))


w3.eth.enable_unaudited_features()
w3.eth.defaultAccount = wallet_address

dict_person = {'0x08f69300323531c6bA0619A2c6892F4FC9482740': 20,
               '0x2E2fa3602696bd889EeD12C4af13d22Cc9E8CC55': 30
              }

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


'''
# 1. Createing items for Auction (qty = 4)
txn_dict = contract.functions.fillitems(4).buildTransaction({
    'chainId': 3,
    'gas': 2000000, #gas_estimate = contract.functions.fillitems(4).estimateGas()
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce,
})
sendtran(txn_dict)
'''



'''
#2. Creating bidders
for person,token in dict_person.items():
    nonce = w3.eth.getTransactionCount(wallet_address)
    txn_dict = contract.functions.register(person, token).buildTransaction({
        'chainId': 3,
        'gas': 2000000, #gas_estimate = contract.functions.fillitems(4).estimateGas()
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce
    })
    sendtran(txn_dict)
'''

'''
#2. Revealing winners
txn_dict = contract.functions.revealWinners().buildTransaction({
    'chainId': 3,
    'gas': 2000000, #gas_estimate = contract.functions.fillitems(4).estimateGas()
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce
})
sendtran(txn_dict)

wincount = contract.functions.getLenWinners().call()

k = 0

while k < wincount:
    print(k, contract.functions.getWinner(k).call())
    k +=1
'''


'''
amount_in_wei = w3.toWei(0.1,'ether')
txn_dict = contract.functions.transfer(wallet_address, amount_in_wei).buildTransaction({
    'chainId': 3,
    'gas': 2000000, #gas_estimate = contract.functions.fillitems(4).estimateGas()
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce
})
sendtran(txn_dict)
'''

'''
txn_dict = contract.functions.kill().buildTransaction({
    'chainId': 3,
    'gas': 2000000, #gas_estimate = contract.functions.fillitems(4).estimateGas()
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce
})
sendtran(txn_dict)
'''


'''
# this transaction will recieve unnamed function
amount_in_ether = 0.01
txn_dict = {
            'to': contract_address,
            'value': w3.toWei(amount_in_ether,'ether'),
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
            'chainId': 3
    }
'''


