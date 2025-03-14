from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from tronpy.exceptions import AddressNotFound

from django.conf import settings


class TronTransaction:
    def __init__(self):
        # self.tron = Tron(network='mainnet')
        # self.tron = Tron(network='nile')
        self.tron = Tron(provider=HTTPProvider(api_key="679bbd65-8f55-4427-86a2-e4a4250be584"))
        self.usdt_contract = self.tron.get_contract(settings.USDT_CONTRACT)

    def generate_address(self):
        return self.tron.generate_address()

    def get_tron_balance(self, address):
        try:
            balance = self.tron.get_account_balance(address)
        except AddressNotFound:
            balance = 0
        return round(balance, 2)

    def get_usdt_balance(self, address):
        try:
            balance = self.usdt_contract.functions.balanceOf(address)
        except AddressNotFound:
            balance = 0
        return round(balance / (10 ** 6), 2)

    def transfer_usdt(self, sender, private_key, recipient, amount):
        tron_key = PrivateKey(bytes.fromhex(private_key))
        usdt_contract = self.tron.get_contract(settings.USDT_CONTRACT)

        txn = (
            usdt_contract.functions.transfer(recipient, int(amount * 1000000))
                .with_owner(sender)
                .fee_limit(40_000_000)
                .build()
                .sign(tron_key)
        )

        tx_hash = txn.broadcast().wait()
        tx_info = self.tron.get_transaction_info(tx_hash['id'])
        return tx_hash

    def transfer_tron(self, sender, private_key, recipient, amount):
        tron_key = PrivateKey(bytes.fromhex(private_key))
        amount_in_sun = int(amount * 1_000_000)

        txn = (
            self.tron.trx.transfer(sender, recipient, amount_in_sun)
                .with_owner(sender)
                .fee_limit(40_000_000)
                .build()
                .sign(tron_key)
        )

        tx_hash = txn.broadcast().wait()
        tx_info = self.tron.get_transaction_info(tx_hash['id'])
        return tx_info

    def get_account(self, address):
        account_info = self.tron.get_account(address)
        return account_info
