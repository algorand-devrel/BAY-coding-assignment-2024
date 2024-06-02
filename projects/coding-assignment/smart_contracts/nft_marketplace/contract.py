# pyright: reportMissingModuleSource=false
from algopy import *

class NftMarketplace(arc4.ARC4Contract):
   

    def __init__(self) -> None:
        "문제 1 시작"
        self.asset_id = UInt64(0)
        self.unitary_price = UInt64(0)
        self.bootstrapped = False
        "문제 1 끝"

    "문제 2 시작"

    @arc4.abimethod
    def bootstrap(
        self, asset: Asset, unitary_price: UInt64, mbr_pay: gtxn.PaymentTransaction
    ) -> None:
        assert Txn.sender == Global.creator_address
        assert self.bootstrapped == False
        assert mbr_pay.receiver == Global.current_application_address
        assert mbr_pay.amount == Global.min_balance + Global.asset_opt_in_min_balance

        self.asset_id = asset.id
        self.unitary_price = unitary_price
        self.bootstrapped = True

        itxn.AssetTransfer(
            xfer_asset = asset,
            asset_amount = 0,
            asset_receiver = Global.current_application_address,
        ).submit()
        "여기에 코드 작성"

    "문제 2 끝"
    "문제 3 시작"

    @arc4.abimethod
    def buy(
        self,
        buyer_txn: gtxn.PaymentTransaction,
        quantity: UInt64,
    ) -> None:
        "여기에 코드 작성"
        assert self.bootstrapped
        assert buyer_txn.sender == Txn.sender
        assert buyer_txn.receiver == Global.current_application_address
        assert buyer_txn.amount == self.unitary_price * quantity

        itxn.AssetTransfer(
            xfer_asset=self.asset_id,
            asset_receiver=buyer_txn.sender,
            asset_amount=quantity,
        ).submit()

    "문제 3 끝"  

    "문제 4 시작"

    @arc4.abimethod(allow_actions=["DeleteApplication"])
    def withdraw_and_delete(self) -> None:
        "여기에 코드 작성"
        assert Txn.sender == Global.creator_address

        itxn.AssetTransfer(
            xfer_asset=self.asset_id,
            asset_receiver=Txn.sender,
            asset_close_to=Txn.sender,
        ).submit()

        itxn.Payment(
            receiver=Txn.sender,
            close_remainder_to=Txn.sender,
        ).submit()

    "문제 4 끝"