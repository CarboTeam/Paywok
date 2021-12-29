# Paywok
Bitcoin payroll system for recurring crypto payments. Pay employees, freelancers, service providers and others monthly or biweekly.

# Installation and Setup
###### `pip install -r requirements.txt`

### On Linux / Mac OS:
###### `python3 manage.py makemigrations`
###### `python3 manage.py migrate`
###### `python3 manage.py createsuperuser`
###### `python3 manage.py runserver`

### On Windows:
###### `python manage.py makemigrations`
###### `python manage.py migrate`
###### `python manage.py createsuperuser`
###### `python manage.py runserver`

### Go to Admin panel:

http://127.0.0.1:8000/admin

#### And open 'Crypto' -> 'Receivers' to add and manage receivers info
Once all receivers added, a scheduler must be set. 

