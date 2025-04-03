FROM python:3.14.0a6-bookworm

RUN apt-get update

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code

EXPOSE 8080
CMD ["python3", "./server.py"]
