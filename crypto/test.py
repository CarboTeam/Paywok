import sys
from pathlib import Path
import os
import django

BASE_DIR = Path(__file__).resolve().parent.parent.resolve()
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paywok.settings')
django.setup()

from crypto.tasks import (provide_payment, provide_payment_testnet)

provide_payment_testnet()
