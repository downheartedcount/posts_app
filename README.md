# FastAPI JSONPlaceholder Sync App

## Описание

Это асинхронное веб-приложение на FastAPI, которое синхронизирует посты и пользователей с внешнего API [`https://jsonplaceholder.typicode.com`](https://jsonplaceholder.typicode.com). Данные сохраняются в PostgreSQL. Реализован REST API для получения постов с фильтрацией по авторам, названию и другим полям.

Приложение:
- полностью асинхронное
- использует Pydantic, SQLAlchemy, HTTPX
- конфигурируется через `.env` и Docker secrets
- запускает фоновую синхронизацию каждые 24 часа через APScheduler

---

## Технологии

- Python 3.11
- FastAPI
- PostgreSQL 15
- SQLAlchemy (async)
- HTTPX
- APScheduler
- Docker & Docker Compose

---

## Запуск (Docker)

### Собрать и запустить контейнеры

```bash
make docker-up
```


## Структура проекта

- .
- ├── docker-compose.yml
- ├── Dockerfile
- ├── requirements.txt
- ├── .env
- ├── secrets/
- │   ├── postgres_password.txt
- │   └── database_url.txt
- └── src/
-    ├── main.py
-    ├── db/
-    │   ├── session.py
-    │   ├── repo.py
-    │   └── init_db.py
-    ├── configs/
-    │   ├── app_config.py
-    │   └── db_config.py
-    ├── client/
-    │   └── posts_client.py
-    ├── services/
-    │   └── sync_service.py
-    ├── api/
-    │   └── routes.py
-    ├── models/
-    │   ├── db_models.py
-    │   ├── schemas.py
-    │   └── models.py
-    ├── utils/
-    │   ├── http_client.py
-    │   ├── scheduler.py
-    │   └── dependencies.py
-    └── exceptions.py

## Настройки

```ini
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
SQLALCHEMY_ECHO=false
BASE_URL=https://jsonplaceholder.typicode.com
SYNC_INTERVAL_HOURS=24
```

Путь к .env прописан в Config каждого Pydantic класса (AppConfig, DBConfig).

## Синхронизация

Синхронизация пользователей и постов происходит:

- один раз при старте приложения
- раз в сутки через APScheduler (фоновая задача)
- Обрабатываются дубликаты (insert only new).


## API Endpoints

```bash
GET /posts
```

Фильтры:
- user_id: int
- username: str
- title: str
- skip: int
- limit: int (по умолчанию 100)


```bash
GET /posts?user_id=1&title=qui
```

## Логгирование

```yaml
2025-06-23 04:15:13 [INFO] posts_client: Fetched 100 posts
```

