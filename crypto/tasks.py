from __future__ import absolute_import, unicode_literals
from celery import shared_task
from crypto.models import (PayeeProfile, PaymentReceipts)
from crypto.btc_services import *


@shared_task
def provide_payment():
    #################
    # MAIN #
    #################

    # walletName = ""
    # ensure_bitcoind_running()
    # run_subprocess("/usr/local/bin/bitcoin-cli", "-datadir=/mnt/volume_lon1_01/bitcoin-core", "loadwallet", walletName)

    minFee = getMinFee()
    for payee in PayeeProfile.objects.filter(provide_payment=True).all():
        btc_price = get_btc_price(payee.payment_currency)
        btc_amount = convert_to_btc(payee.payment_amount, btc_price)

        bitcoin_cli_call("-datadir=/mnt/volume_lon1_01/bitcoin-core",
                         "-named",
                         "sendtoaddress",
                         "address=" + payee.btc_address,
                         "amount=" + str(btc_amount), "fee_rate=" + str(minFee))
        new_receipt = PaymentReceipts(user_profile=payee,
                                      btc_amount=btc_amount,
                                      btc_fee_amount=minFee / (10 ** 8),
                                      fee_amount=convert_from_btc(minFee / (10 ** 8), btc_price),
                                      btc_price=btc_price,
                                      payment_network='M')
        new_receipt.save()


@shared_task
def provide_payment_testnet():
    #################
    # TESTNET #
    #################

    # walletName = ""
    # ensure_bitcoind_running()
    # run_subprocess("/usr/local/bin/bitcoin-cli", "-datadir=/mnt/volume_lon1_01/bitcoin-core", "loadwallet", walletName)

    minFee = getMinFee()
    for payee in PayeeProfile.objects.filter(provide_payment=True).all():
        btc_price = get_btc_price(payee.payment_currency)
        btc_amount = convert_to_btc(payee.payment_amount, btc_price)

        bitcoin_cli_call("-datadir=/mnt/volume_lon1_01/bitcoin-core",
                         "-testnet",
                         "-named",
                         "sendtoaddress",
                         "address=" + payee.btc_address,
                         "amount=" + str(btc_amount), "fee_rate=" + str(minFee))
        new_receipt = PaymentReceipts(user_profile=payee,
                                      btc_amount=btc_amount,
                                      btc_fee_amount=minFee / (10 ** 8),
                                      fee_amount=convert_from_btc(minFee / (10 ** 8), btc_price),
                                      btc_price=btc_price,
                                      payment_network='T')
        new_receipt.save()
