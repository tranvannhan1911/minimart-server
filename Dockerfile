FROM ubuntu:20.04

WORKDIR /app

RUN apt update -y

RUN apt install git gcc g++ make python3-dev \
    python3-pip libxml2-dev libxslt1-dev zlib1g-dev \
    libmysqlclient-dev gettext curl -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]

