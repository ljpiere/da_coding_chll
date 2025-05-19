# Dockerfile
FROM python:3.11-slim
WORKDIR /code
COPY pyproject.toml poetry.lock /code/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev
COPY . /code
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
