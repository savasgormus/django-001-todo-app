- python -m venv env
- .\env\Scripts\activate
- pip install django
- pip install python-decouple
- django-admin startproject main .
- py manage.py migrate
- py manage.py runserver
- py manage.py startapp todo


- decouple ile secretkey'i .env dosyasına kaydettik. app'imizi settings.py dosyasına girdik.