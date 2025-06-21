FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt


FROM python:3.11-slim

RUN useradd --create-home appuser

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY ./src /app/src
COPY .env /app/

ENV PYTHONPATH=/app

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD bash -c "python src/db/init_db.py && uvicorn src.main:app --host 0.0.0.0 --port 8000"
