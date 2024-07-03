FROM python:3.10.11

WORKDIR /code

COPY ./ /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt