FROM python:3-slim

ADD . /app

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libmariadb-dev-compat mariadb-client
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "/bin/bash", "-c", "/app/scripts/start_server.sh" ]
