FROM python:3.12-slim

WORKDIR /app

# УСТАНОВКА СИСТЕМНЫХ ЗАВИСИМОСТЕЙ
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libffi-dev \
    libc-dev \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*


# ЗАБРОС ЗАВИСИМОСТЕЙ
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# КОПИРУЕМ ПРОЕКТ
COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
