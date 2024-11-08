FROM python:3.11-bullseye AS server-base

ENV PYTHONBUFFERED 1

RUN apt-get update -y  \
    && apt-get install -y postgresql-client  \
    && pip install --upgrade pip \
    && apt-get clean

WORKDIR /usr/src/backend/

COPY requirements.txt /usr/src/backend/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/backend/

FROM server-base AS server

#ENTRYPOINT ["sh", "./scripts/migrations.sh"]
