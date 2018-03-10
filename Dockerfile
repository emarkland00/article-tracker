FROM python:3.7.0a2-alpine3.6

LABEL maintainer="Errol Markland"

RUN mkdir -p /usr/app
WORKDIR /usr/app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/

# Copy config file (must manually supply!)
COPY config.ini src/config.ini

CMD ["python", "src/main.py"]
