from tronpy import Tron
from tronpy.keys import PrivateKey


tron = Tron(network='nile')

def trx_transfer_usdt(sender, private_key, recipient, amount):
    tron_key = PrivateKey(bytes.fromhex(private_key))
    usdt_contract = tron.get_contract("TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf")
    txn = (
        usdt_contract.functions.transfer(recipient, int(amount * 1000000))
        .with_owner(sender)
        .fee_limit(100_000_000)
        .build()
        .sign(tron_key)
    )
    result = txn.broadcast()
    return result
