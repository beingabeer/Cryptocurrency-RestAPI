# Cryptocurrency-RestAPI

A simple Rest API for tracking cryptocurrency built using django rest framework

Install dependencies:

```
python3 -m pip3 install -r requirements.txt
```

then run following commands:

```
python3 manage.py makemigrations trackingAPI
python3 manage.py migrate
python3 manage.py runserver
```
and finally start the celery worker:

```
celery -A cryptocurrencytracking worker -l info
```
