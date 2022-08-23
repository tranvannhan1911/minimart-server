FROM ubuntu:20.04

WORKDIR /app

ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update -y

RUN apt install git gcc g++ make python3-dev -y
RUN apt install python3-pip -y
RUN apt install libmysqlclient-dev gettext curl -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]

