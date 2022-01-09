<img src="./logo.svg"  width="300">

Paywok is a bitcoin-based payroll system which can be used to pay employees, freelancers and service providers on a regular basis, for example monthly or biweekly. Paywok also produces receipts that you can use for accounting purposes.

Technically, Paywok uses the Django admin panel as a frontend to interact with a Python script that then uses Bitcoin Core's ```bitcoin-cli``` to make transactions. Bitcoin operations take place in the ```crypto/tasks.py``` file using the util functions from ```crypto/btc_services.py```.

# Table of contents
- [Table of contents](#table-of-contents)
- [Requirements](#requirements)
- [Bitcoin Core installation and setup](#bitcoin-core-installation-and-setup)
  * [Download and install Bitcoin Core](#download-and-install-bitcoin-core)
  * [Download the blockchain](#download-the-blockchain)
  * [Create and fund the wallet](#create-and-fund-the-wallet)
- [Redis installation and setup](#redis-installation-and-setup)
  * [Install Redis](#install-redis)
  * [Starting Redis](#starting-redis)
  * [Check if Redis is working](#check-if-redis-is-working)
- [Python-Django and Paywok installation](#python-django-and-paywok-installation)
  * [Install python and download Paywok](#install-python-and-download-paywok)
  * [Install packages](#install-packages)
  * [Create an admin user](#create-an-admin-user)
  * [Django run command](#django-run-command)
  * [Celery run command](#celery-run-command)
  * [Celery Beat run command](#celery-beat-run-command)
- [Paywok configuration via the Django admin panel](#paywok-configuration-via-the-django-admin-panel)
  
# Requirements

We've tested these instructions on Linux (specifically Ubuntu 20.04). However, Paywok should work on any OS that's supported by Bitcoin Core and Redis. 
- [Bitcoin Core](https://bitcoin.org/en/download) running as a full node, which means you will need at least 400 GB of disk space to download the blockchain, and a reasonably fast machine. For more information, please see https://bitcoin.org/en/full-node. 
- [python 3.x](https://www.python.org/downloads/)
- [redis](https://redis.io/download)

# Bitcoin Core installation and setup
## Download and install Bitcoin Core

You can find detailed installation instructions at https://bitcoin.org/en/full-node#linux-instructions, but we've included a summary here. 

We recommend downloading and uncompressing Bitcoin Core in the temp directory:

```cd /tmp```

As of this writing (January 2022), the latest Bitcoin Core version is 22.0. You should always use the latest version. 

```wget https://bitcoin.org/bin/bitcoin-core-22.0/bitcoin-22.0-x86_64-linux-gnu.tar.gz -O bitcoin.tar.gz```

Let's uncompress the file we just downloaded:

``` tar -xvf bitcoin.tar.gz```

Now we can install Bitcoin Core:

``` sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-22.0/bin/*```

Finally, let's check our Bitcoin Core version check to make sure we did everything correctly:

``` bitcoind --version```


## Download the blockchain

For simplicity, these instructions assume you're using the same machine to run Django and Bitcoin Core. You might want to use different machines for various reasons (security, hard drive requirements, etc). In any case, you will need to fund your wallet.

Before creating the wallet, we first need to download the blockchain:

``` bitcoind --daemon```

This will run ``` bitcoind``` on the background. You will need to wait till the synchronization is complete, which might take hours or even days depending on your internet speed and hardware. You can check the progress with this command: 

``` bitcoin-cli getblockchaininfo```

The output will be something like this:
```
  "chain": "test",
  "blocks": 2134480,
  "headers": 2134480,
  "bestblockhash": "000000000000008129a36fbbe69f74ff2cd25f534bb63d637ba2afa211297f11",
  "difficulty": 26179695.47502262,
  "mediantime": 1641213662,
  "verificationprogress": 0.9999999620579896,
```

When ```verificationprogress``` is extremely close to 1 (like in the example above), we can assume that the blockchain is fully downloaded.

## Create and fund the wallet

After we've downloaded and fully synchronized the blockchain, we can create the wallet that we'll use for payments:

```bitcoin-cli createwallet paywokWallet```

Then we'll need a receiving address:

```bitcoin-cli getnewaddress```

You can now use your favorite wallet to send bitcoin to the receiving address. After the transaction is complete, you should be able to see the new balance using the following command:

```bitcoin-cli getbalances```

You will be using this balance to pay all your payees (employees, freelancers, service providers, etc), so make sure there's enough for your first payment. After you've checked that everything works well, you should fund the wallet with enough bitcoin to make your payments. 

# Redis installation and setup

You can find the Redis quick start document [here](https://redis.io/topics/quickstart), but we've included a summary below.

## Install Redis
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
```
## Starting Redis
```
redis-server
```
## Check if Redis is working
```
$ redis-cli ping
PONG
```

# Python-Django and Paywok installation

## Install python and download Paywok
Paywok uses python 3.10. Please check if your distro already uses that version of python, otherwise you can download it [here](https://www.python.org/downloads/).

Then download this git project:

```git clone https://github.com/CarboTeam/Paywok.git```

Then run the following commands in the ```Paywok``` folder:

## Install packages
```pip install -r requirements.txt```

```python3 manage.py makemigrations```

```python3 manage.py migrate```

## Create an admin user
```python3 manage.py createsuperuser```

## Django run command
```python3 manage.py runserver```

## Celery run command
```celery -A paywok worker --loglevel=INFO```

## Celery Beat run command
```celery -A paywok beat --scheduler django_celery_beat.schedulers:DatabaseScheduler```

# Paywok configuration via the Django admin panel

You can access Paywok here:

http://localhost:8000/admin

Go to 'CRYPTO' -> 'Payees' to add your payees. 

Once you've added payees, you must configure a periodic task to automatically make the payments.

Go to 'PERIODIC TASKS' -> 'Periodic tasks'. 

Click 'Add periodic task' (top right). 

In the 'Task (registered)' field, select _crypto.tasks.provide_payment_ for Bitcoin mainnet payments or _crypto.tasks.provide_payment_testnet_ to test payments on the Bitcoin testnet. We recommend starting with the Bitcoin testnet. 
The 'Task (custom)' field can be left blank since it will autofil with the content of the registered task we just input. 

In the 'Schedule' section, you'll see several scheduling options. We recommend the 'Crontab Schedule' since it offers more personalization. 

If you are not familiar with Cron, check out this [guide](https://crontab.guru/).

Basically, the format is as follows:
- minute        (0-59)
- hour          (0-23)
- day of month  (1-31)
- month         (1-12)
- day of week   (0-7)

An asterisk in any of the fields' means that the task will run every minute/hour/day/month/day-of-week.

Examples:
- The 21st of every month at 8pm: 0 20 21 * *
- Every Sunday at midnight: 0 0 * * 0

Don't forget to save your periodic task.

If you did everything correctly, the payment(s) will go out according to the schedule and you will be able to download the receipts from the Django/Paywok admin panel (Receipts, under Crypto).
