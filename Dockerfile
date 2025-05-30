FROM python:3.11-slim

# Установим curl, чтобы скачать Poetry официально
RUN apt-get update && apt-get install -y curl

# Установка Poetry через официальный install-скрипт
RUN curl -sSL https://install.python-poetry.org | python3 -

# Обновим PATH (чтобы poetry был доступен)
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]