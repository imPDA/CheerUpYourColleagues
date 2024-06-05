FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt install -y python3 && \
    pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml .
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY ./app /app

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"