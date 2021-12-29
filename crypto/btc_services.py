import argparse
import json
from collections import OrderedDict
from decimal import Decimal
import shlex
import subprocess
import time
import requests


def verbose(content):
    print(content)


def run_subprocess(exe, *args):
    """
    Run a subprocess (bitcoind or bitcoin-cli)
    Returns => (command, return code, output)

    exe: executable file name (e.g. bitcoin-cli)
    args: arguments to exe
    """
    cmd_list = [exe] + list(args)
    verbose("bitcoin cli call:\n  {0}\n".format(" ".join(shlex.quote(x) for x in cmd_list)))
    with subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1024) as pipe:
        output, _ = pipe.communicate()
    try:
        output = output.decode('ascii')
    except Exception as e:
        print(e)    retcode = pipe.returncode
    verbose("bitcoin cli call return code: {0}  output:\n  {1}\n".format(retcode, output))
    return (cmd_list, retcode, output)


def bitcoin_cli_call(*args):
    """
    Run `bitcoin-cli`, return OS return code
    """
    _, retcode, _ = run_subprocess("/usr/local/bin/bitcoin-cli", *args)
    return retcode


def bitcoin_cli_checkoutput(*args):
    """
    Run `bitcoin-cli`, fail if OS return code nonzero, return output
    """
    cmd_list, retcode, output = run_subprocess("/usr/local/bin/bitcoin-cli", *args)
    if retcode != 0:
        raise subprocess.CalledProcessError(retcode, cmd_list, output=output)
    return output


def bitcoind_call(*args):
    """
    Run `bitcoind`, return OS return code
    """
    _, retcode, _ = run_subprocess("/usr/local/bin/bitcoind", *args)
    return retcode


def ensure_bitcoind_running():
    """
    Start bitcoind (if it's not already running) and ensure it's functioning properly
    """
    # start bitcoind.  If another bitcoind process is already running, this will just print an error
    # message (to /dev/null) and exit.

    if isTestnet:
        bitcoind_call("-daemon", "-testnet")
    else:
        bitcoind_call("-daemon")
    # verify bitcoind started up and is functioning correctly
    times = 0
    while times <= 100:
        times += 1
        if isTestnet:
            if bitcoin_cli_call("-testnet", "getnetworkinfo") == 0:
                return
        else:
            if bitcoin_cli_call("getnetworkinfo") == 0:
                return
        time.sleep(0.5)

    raise Exception("Timeout while starting bitcoin server")


def get_btc_price(currency):
    # currency can be "USD" or "EUR", otherwise null is returned.
    if currency not in ['USD', 'EUR']:
        return "error"
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    x = requests.get(url)
    string = x.json().get("bpi").get(currency).get("rate")
    btc_price = ''
    for i in range(0, len(string)):
        if string[i] == ',':
            btc_price += ''
        else:
            btc_price += string[i]
    return float(btc_price)


def convert_to_btc(amount, btc_price):
    btc_amount = amount / btc_price
    return round(btc_amount, 8)


def convert_from_btc(btc_amount, btc_price):
    usd_amount = btc_amount * btc_price
    return round(usd_amount, 2)


def getMinFee():
    url = "https://mempool.space/api/v1/fees/recommended"
    x = requests.get(url)
    return x.json().get("minimumFee")
