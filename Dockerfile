FROM python:2.7.14

MAINTAINER Errol Markland

RUN apt-get install gcc
RUN mkdir -p /usr/app
WORKDIR /usr/app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/

# Copy config file (must manually supply!)
COPY config.ini src/config.ini

CMD ["python", "src/main.py"]
