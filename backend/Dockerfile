FROM python:3.7-slim

WORKDIR app

COPY ../ .

RUN python -m pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip3 install -r /app/requirements.txt --no-cache-dir


CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]