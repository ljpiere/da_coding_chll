# ───────── Etapa 1: builder ─────────
FROM python:3.11-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*
ENV POETRY_VERSION=1.7.1 POETRY_VIRTUALENVS_CREATE=false POETRY_NO_INTERACTION=1
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src
COPY pyproject.toml poetry.lock* /src/

# fuerza consistencia (regenera solo si hace falta)
# RUN poetry lock --check || poetry lock --no-update

RUN poetry install --only main --no-root

# ───────── Etapa 2: runtime ─────────
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

# Dependencias ya compiladas
COPY --from=builder /usr/local/lib/python3.11/site-packages \
                    /usr/local/lib/python3.11/site-packages
# (Poetry no se copia porque no hace falta)
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /code
COPY . /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
