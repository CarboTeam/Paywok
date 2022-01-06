# Paywok

Paywok is a bitcoin-based payroll system. You can use Paywok to pay employees, freelancers and service providers on a regular basis, for example monthly or biweekly.

Technically, Paywok uses the Django admin panel as a frontend to interact with a Python script that then uses Bitcoin Core's ```bitcoin-cli``` to make transactions. Bitcoin operations take place in the ```crypto/tasks.py``` file using the util functions from ```crypto/btc_services.py```

# Table of contents
- [Paywok](#paywok)
- [Table of contents](#table-of-contents)
- [Requirements](#requirements)
- [Bitcoin Core installation and setup](#bitcoin-core-installation-and-setup)
  * [Download and install Bitcoin Core](#download-and-install-bitcoin-core)
  * [Download the blockchain](#download-the-blockchain)
  * [Create and fund the wallet](#create-and-fund-the-wallet)
- [Redis installation and setup](redis-installation-and-setup)
  * [Install redis](#install-redis)
  * [Run redis-server](#run-redis-server)
  * [Check if Redis is working](#check-if-redis-is-working)
- [Python and Django installation and setup](#python-and-django-installation-and-setup)
  * [Install python](#install-python)
  * [Install packages](#install-packages)
  * [Create admin user](#create-admin-user)
  * [Django run command](#django-run-command)
  * [Celery run command](#celery-run-command)
  * [Celery Beat run command](#celery-beat-run-command)
  * [Django Admin panel operations](#django-admin-panel-operations)
  
# Requirements

- We've tested these instructions on Linux (specifically Ubuntu 20.04). However, Paywok should work on any OS that's supported by Bitcoin Core and Redis. 
- [Bitcoin Core](https://bitcoin.org/en/download) running as a full node, which means you will need at least 400 GB of disk space to download the blockchain, and a reasonably fast machine. For more information, please head over to https://bitcoin.org/en/full-node. 
- [python 3.x](https://www.python.org/downloads/)
- [redis](https://redis.io/download)

# Bitcoin Core installation and setup
## Download and install Bitcoin Core

You can find detailed installation instructions at https://bitcoin.org/en/full-node#linux-instructions, but we've included a summary here. 

We recommend downloading and uncompressing Bitcoin Core in the temp directory:

```cd /tmp```

As of this writing (January 2022), the latest Bitcoin Core version is 22.0. You should always use the latest version. 

```wget https://bitcoin.org/bin/bitcoin-core-22.0/bitcoin-22.0-x86_64-linux-gnu.tar.gz -O bitcoin.tar.gz```

Do this to uncompress the file you just downloaded:

``` tar -xvf bitcoin.tar.gz```

Now you can install Bitcoin Core:

``` sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-22.0/ /bin/*```

Finally, let's check our Bitcoin Core version check to make sure we did everything correctly:

``` bitcoind --version```


## Download the blockchain

For simplicity, these instructions assume you're using the same machine to run Django and Bitcoin Core. You might want to use different machines for various reasons (security, hard drive requirements, etc). In any case, you will need to fund your wallet.

Before creating the wallet, we first need to download the blockchain:

``` bitcoind --daemon```

This will run ``` bitcoind``` on the background. 

You will need to wait till the synchronization is complete, which might take hours or even days depending on your internet speed and hardware. You can check how's it going with this command: 

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

When ```verificationprogress``` is really, really close to 1 (like in the example above), we can assume that the blockchain is fully downloaded.

## Create and fund the wallet

After you've downloaded and fully synchronized the blockchain, you can create the wallet that you'll use for payments:

```bitcoin-cli createwallet paywokWallet```

Then you'll need a receiving address:

```bitcoin-cli getnewaddress```

You can now use your favorite wallet to send bitcoin to the receiving address. After the transaction is complete, you should be able to see the new balance using the following command:

```bitcoin-cli getbalances```

You will be using this balance to pay all your payees (employees, freelancers, service providers, etc), so make sure there's enough for your first payment. After you've checked that everything works well, you might want to fund the wallet with a few months' worth of payments. 
# Redis installation and setup

## Install redis
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
```
## Run redis-server
```
redis-server
```
## Check if Redis is working
```
redis-cli ping
PONG
```
You can find full Redis Quick Start instructions [here](https://redis.io/topics/quickstart)

# Python and Django installation and setup

## Install python 3.x.y
Project was created using python 3.10, which you can find and download [here](https://www.python.org/downloads/)

Then download this git project:

```git clone https://github.com/CarboTeam/Paywok.git```

and run next commands in ```Paywok``` folder

## Install packages
```pip install -r requirements.txt```

```python3 manage.py makemigrations```

```python3 manage.py migrate```

## Create admin user
```python3 manage.py createsuperuser```

## Django run command
```python3 manage.py runserver```

## Celery run command
```celery -A paywok worker --loglevel=INFO```

## Celery Beat run command
```celery -A paywok beat --scheduler django_celery_beat.schedulers:DatabaseScheduler```

## Django Admin panel operations

You can access it here:

http://localhost:8000/admin

Or, if you are using a hosting company:

http://<IPofYourServer>:8000/admin

Open the tab 'CRYPTO' -> 'Payees' to add and manage payees info
Once all desired payees are added, a scheduler must be set to automatically make the payments.

Open the tab 'PERIODIC TASKS' -> 'Periodic tasks'

In 'Task (registered)' select _crypto.tasks.provide_payment_ for mainnet payments or _crypto.tasks.provide_payment_testnet_ to make payments on the Bitcoin testnet.

In the 'Schedule' fields, there are several options. We recommend the 'Crontab Schedule' since it offers more personalization. 

If you are not familiar with Cron, check out this quick [guide](https://crontab.guru/)

Basically, the format is as follows:
- minute        (0-59)
- hour          (0-23)
- day of month  (1-31)
- month         (1-12)
- day of week   (0-7)

Where an asterisc in any of the fields means to do it in every minute/hour/day/month/day-of-week

Examples:
- The 21st of every month at 8:00 pm: 0 20 21 * *
- Every Sunday at midnight (00:00 am): 0 0 * * 0

Click save and close the Admin browser tab. 
If everything was done correctly, payments will be made automatically when indicated 
