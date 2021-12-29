# Paywok
Payroll system for recurring Bitcoin payments. Pay employees, freelancers, service providers and others monthly or biweekly.

How does it work?

Paywok uses the Django Admin panel as a frontend to interact with a python script which uses ```bitcoin-cli``` to make transactions. 
All the Bitcoin actions take place in the file ```crypto/tasks.py``` using the util functions from ```crypto/btc_services.py```

# Requirements
- [python 3.x](https://www.python.org/downloads/)
- [redis](https://redis.io/download)
- [Bitcoin Core](https://bitcoin.org/en/download) with a full node (whole blockchain downloaded)

# Bitcoin Core Installation

Opening the temporary directory:

```cd /tmp```

Now we need to install the tar file.

This commands installs version 22.0 (latest as of the date this was written).
In order to download latest versions, we would need to change every intance of "22.0" by whatever release we are trying to download. 

```wget https://bitcoin.org/bin/bitcoin-core-22.0/bitcoin-22.0-x86_64-linux-gnu.tar.gz -O bitcoin.tar.gz```

Uncompressing the downloaded file:

``` tar -xvf bitcoin.tar.gz```

Installing:

``` sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-22.0/ /bin/*```

Finally, to check we did everything correctly, this should give us the version of Bitcoin Core we just installed:

``` bitcoind --version```


# Funding the wallet

Before creating the wallet, we first need to download the full Blockchain in order to do so, we just have to run the following command:

``` bitcoind --daemon```

This will start the program and it will be running on the background. 

In order to check when the synchronization is complete, we run this command: 

``` bitcoin-cli getblockchaininfo```

And the output will be something like this:
```
  "chain": "test",
  "blocks": 2134480,
  "headers": 2134480,
  "bestblockhash": "000000000000008129a36fbbe69f74ff2cd25f534bb63d637ba2afa211297f11",
  "difficulty": 26179695.47502262,
  "mediantime": 1641213662,
  "verificationprogress": 0.9999999620579896,
```

When ```verificationprogress``` is really, really close to 1 (it will likely never reach) the we can say the blockchain is fully downloaded. 
(The blockchain can take up 2 weeks to fully download depending on internet speed and hardware used)

To create a wallet:

```bitcoin-cli createwallet paywokWallet```

To get a new address:

```bitcoin-cli getnewaddress```

If you send bitcoin to the given address and wait one blockchain confirmation, running the following command should give you your balance:

```bitcoin-cli getbalances```


# Installation and Setup
###### Install packages
```pip install -r requirements.txt```

```python3 manage.py makemigrations```

```python3 manage.py migrate```

###### Create admin user
```python3 manage.py createsuperuser```

###### Django run command
```python3 manage.py runserver```

###### Celery run command
```celery -A paywok worker --loglevel=INFO```

###### Celery Beat run command
```celery -A paywok beat --scheduler django_celery_beat.schedulers:DatabaseScheduler```

### Go to Admin panel:

http://localhost:8000/admin

Or, if you are using a hosting company:

http://<IPofYourServer>:8000/admin

#### Open the tab 'CRYPTO' -> 'Payees' to add and manage payees info
Once all desired payees are added, a scheduler must be set to automatically make the payments.

#### Open the tab 'PERIODIC TASKS' -> 'Periodic tasks'

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

#### Examples:
- The 21st of every month at 8:00 pm: 0 20 21 * *
- Every Sunday at midnight (00:00 am): 0 0 * * 0

Click save and close the Admin browser tab. 
If everything was done correctly, payments will be made automatically when indicated 
