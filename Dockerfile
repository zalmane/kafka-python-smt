FROM python:3.8-slim-buster

WORKDIR /core

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV PYTHONPATH=/app
CMD [ "python3","-u", "smt_runner.py"]