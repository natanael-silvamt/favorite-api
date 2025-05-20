FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install poetry===2.1.3

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock alembic.ini .env ./

RUN poetry install --no-root

COPY README.md .

RUN pip install fastapi uvicorn

COPY . .
