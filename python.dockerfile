FROM python:3

WORKDIR /var/www/django

COPY ./requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt