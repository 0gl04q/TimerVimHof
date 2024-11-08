#!/bin/sh
until pg_isready --host="${DB_HOST}" --username="${POSTGRES_USER}"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - moving to up app"
alembic upgrade head
uvicorn main:app --host=0.0.0.0 --port=8000 --reload