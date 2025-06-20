# mini_CRM_app

Мой первый pet-проект на FastAPI — простой mini CRM с асинхронной архитектурой, базовой безопасностью и тестами.

## О чём проект

Минималистичная CRM-система для учёта пользователей, клиентов и сделок. Всё делал сам, чтобы разобраться, как строится бэкенд “с нуля”:  
- Асинхронный FastAPI + SQLAlchemy (async)  
- Alembic для миграций  
- Docker и Docker Compose для запуска  
- Валидация и базовые проверки  
- JWT для авторизации  
- Всё разбито по модулям (user, client, deal, security, core)  
- Права через Enum ролей (user, manager, admin, superuser)

## Как запустить

```bash
# Клонируй проект
git clone https://github.com/Nakivaykkka/mini-crm.git
cd mini_CRM_app

# Создай .env на основе .env.example (или сразу свой)
cp .env.example .env

# Собери и подними всё через Docker
docker-compose up --build -d

# Накати миграции внутри контейнера
docker-compose exec app alembic upgrade head

# Проверь работу через Swagger
# По умолчанию: http://localhost:8000/docs
