from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

CURRENCIES = [
    ('USD', 'United States Dollar'),
    ('EUR', 'Euro'),
]
NETWORKS = [
    ('M', 'Mainnet'),
    ('T', 'Testnet'),
]


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PayeeProfile(TimeStampMixin):
    # for notification
    email = models.EmailField(verbose_name='Email address', blank=True)
    # personal data for receipt
    first_name = models.CharField(verbose_name='First name', max_length=255)
    last_name = models.CharField(verbose_name='Last name', max_length=255)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=15, blank=True)
    # Home Address
    home_address1 = models.CharField(verbose_name='Home Address 1', blank=True, max_length=1023)
    home_address2 = models.CharField(verbose_name='Home Address 2', blank=True, max_length=1023)
    home_city = models.CharField('City', max_length=30, blank=True)
    home_zip = models.CharField('Home ZIP', max_length=7, blank=True)
    home_province = models.CharField('Province', max_length=30, blank=True)
    home_country = models.CharField('Country', max_length=20, blank=True)

    national_id = models.CharField(verbose_name='National ID', max_length=255, blank=True)
    taxpayer_id = models.CharField(verbose_name='Tax Payer ID', max_length=255, blank=True)
    btc_address = models.CharField(verbose_name='BTC address', max_length=63)
    payment_amount = models.FloatField('Payment amount')
    payment_currency = models.CharField('Currency', max_length=3, choices=CURRENCIES, default="USD")

    # company data for receipt
    title = models.CharField(verbose_name='Title', blank=True, max_length=127)
    company = models.CharField(verbose_name='Company', blank=True, max_length=127)
    company_id = models.CharField(verbose_name='Company ID', blank=True, max_length=127)

    # Business Address
    business_address1 = models.CharField(verbose_name='Business Address 1', blank=True, max_length=1023)
    business_address2 = models.CharField(verbose_name='Business Address 2', blank=True, max_length=1023)
    business_city = models.CharField('City', max_length=30, blank=True)
    business_zip = models.CharField('Business ZIP', max_length=7, blank=True)
    business_province = models.CharField('Province', max_length=30, blank=True)
    business_country = models.CharField('Country', max_length=20, blank=True)

    provide_payment = models.BooleanField('Enable payments for this payee', default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Payee'
        verbose_name_plural = 'Payees'


class PaymentReceipts(TimeStampMixin):
    user_profile = models.ForeignKey(PayeeProfile, on_delete=models.CASCADE, related_name='receipts')
    payment_network = models.CharField('Network', max_length=1, choices=NETWORKS, default="T")

    # taken from payee profile
    first_name = models.CharField(verbose_name='First name', max_length=255)
    last_name = models.CharField(verbose_name='Last name', max_length=255)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=15, blank=True)
    national_id = models.CharField(verbose_name='National ID', max_length=255, blank=True)
    taxpayer_id = models.CharField(verbose_name='Tax Payer ID', max_length=255, blank=True)

    # Home Address
    home_address1 = models.CharField(verbose_name='Home Address 1', blank=True, max_length=1023)
    home_address2 = models.CharField(verbose_name='Home Address 2', blank=True, max_length=1023)
    home_city = models.CharField('City', max_length=30, blank=True)
    home_zip = models.CharField('Home ZIP', max_length=7, blank=True)
    home_province = models.CharField('Province', max_length=30, blank=True)

    home_country = models.CharField('Country', max_length=20, blank=True)

    btc_address = models.CharField(verbose_name='BTC address', max_length=63)

    payment_amount = models.FloatField('Payment amount')
    payment_currency = models.CharField('Currency', max_length=3, choices=CURRENCIES, default="USD")

    title = models.CharField(verbose_name='Title', blank=True, max_length=127)
    company = models.CharField(verbose_name='Company', blank=True, max_length=127)
    company_id = models.CharField(verbose_name='Company ID', blank=True, max_length=127)

    business_address1 = models.CharField(verbose_name='Business Address 1', blank=True, max_length=1023)
    business_address2 = models.CharField(verbose_name='Business Address 2', blank=True, max_length=1023)
    business_city = models.CharField('City', max_length=30, blank=True)
    business_zip = models.CharField('ZIP', max_length=7, blank=True)
    business_province = models.CharField('Province', max_length=30, blank=True)
    business_country = models.CharField('Country', max_length=20, blank=True)

    # calculated
    receipt_reference = models.CharField(verbose_name='Receipt Reference', max_length=255, blank=True)

    btc_amount = models.FloatField('Payment amount in BTC')
    fee_amount = models.FloatField('Payment fee amount', default=0)
    btc_fee_amount = models.FloatField('Payment fee amount in BTC', default=0)

    btc_price = models.FloatField('Applied BTC price')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.receipt_reference = f'{len(self.user_profile.receipts.all()) + 1}_{datetime.now().date().year}'
            self.first_name = self.user_profile.first_name
            self.last_name = self.user_profile.last_name
            self.phone_number = self.user_profile.phone_number
            self.national_id = self.user_profile.national_id
            self.taxpayer_id = self.user_profile.taxpayer_id

            self.home_country = self.user.profile.home_country
            self.home_province = self.user.profile.home_province
            self.home_city = self.user.profile.home_city
            self.home_zip = self.user.profile.home_zip
            self.home_address1 = self.user.profile.home_address1
            self.home_address2 = self.user.profile.home_address2

            self.btc_address = self.user_profile.btc_address
            self.payment_amount = self.user_profile.payment_amount
            self.payment_currency = self.user_profile.payment_currency

            self.title = self.user_profile.title
            self.company = self.user_profile.company
            self.company_id = self.user_profile.company_id

            self.business_country = self.user.profile.business_country
            self.business_province = self.user.profile.business_province
            self.business_city = self.user.profile.business_city
            self.business_zip = self.user.profile.business_zip
            self.business_address1 = self.user.profile.business_address1
            self.business_address2 = self.user.profile.business_address2

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Receipt'
        verbose_name_plural = 'Receipts'
