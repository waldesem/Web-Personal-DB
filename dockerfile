FROM python:3.12-slim

WORKDIR /app

# Установка uv
RUN pip install --no-cache-dir uv

# Копируем только pyproject.toml для кэширования зависимостей
COPY pyproject.toml .

# Устанавливаем зависимости — этот слой закешируется, если pyproject.toml не менялся
RUN uv pip install -e .

# Копируем остальной код
COPY . .

ENV FLASK_APP=server_flask.app
ENV FLASK_ENV=production

EXPOSE 8000

CMD ["gunicorn", "wsgi:app"]
