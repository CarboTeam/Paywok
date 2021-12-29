from __future__ import absolute_import, unicode_literals
from celery import shared_task
from crypto.models import (PayeeProfile, PaymentReceipts)
from crypto.btc_services import *


@shared_task
def provide_payment():
    walletName = "paywokWallet"
    ensure_bitcoind_running(False)
    
    # Create new wallet.
    try:
        run_subprocess("/usr/local/bin/bitcoin-cli", "createwallet", walletName)
    except Exception as e:
        print(e)

    #Do "unload wallet" command just in case there is any unwanted wallet loaded up
    run_subprocess("/usr/local/bin/bitcoin-cli", "unloadwallet")
    #Load the freshly created wallet
    run_subprocess("/usr/local/bin/bitcoin-cli", "loadwallet", walletName)

    minFee = getMinFee()
    for payee in PayeeProfile.objects.filter(provide_payment=True).all():
        btc_price = get_btc_price(payee.payment_currency)
        btc_amount = convert_to_btc(payee.payment_amount, btc_price)

        bitcoin_cli_call("-named",
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
    
    walletName = "paywokWalletTest"
    ensure_bitcoind_running(True)
    
    # Create new wallet.
    try:
        run_subprocess("/usr/local/bin/bitcoin-cli", "-testnet", "createwallet", walletName)
    except Exception as e:
        print(e)

    #Do "unload wallet" command just in case there is any unwanted wallet loaded up
    run_subprocess("/usr/local/bin/bitcoin-cli", "-testnet", "unloadwallet")
    #Load the freshly created wallet
    run_subprocess("/usr/local/bin/bitcoin-cli", "-testnet", "loadwallet", walletName)

    minFee = getMinFee()
    for payee in PayeeProfile.objects.filter(provide_payment=True).all():
        btc_price = get_btc_price(payee.payment_currency)
        btc_amount = convert_to_btc(payee.payment_amount, btc_price)

        bitcoin_cli_call("-testnet",
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
