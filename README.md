# FastAPI JSON Sync App

Это веб-приложение на FastAPI, которое синхронизирует посты и пользователей с [JSONPlaceholder](https://jsonplaceholder.typicode.com) раз в сутки, сохраняет их в PostgreSQL и предоставляет REST API с фильтрацией по данным постов и информации об авторах.

---

## Возможности

- Асинхронный стек: `FastAPI + SQLAlchemy + PostgreSQL`
- Ежедневная синхронизация постов и пользователей
- REST API с фильтрацией и пагинацией
- Docker + Docker Compose
- Хранение секретов через `docker secrets`

---

## Стек технологий

- Python 3.11
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- APScheduler
- Docker / docker-compose
- Pydantic v2

---

## Установка и запуск

### Требования

- Docker + Docker Compose

### Сборка и запуск

```bash
make docker-up
```
Это:

- соберёт образ
- поднимет PostgreSQL
- создаст таблицы
- запустит FastAPI на http://localhost:8000


### Остановка и удаление

```bash
make docker-down
```


### Структура проекта
- .
- ├── src/
- │   ├── api/              # Роуты
- │   ├── client/           # HTTP клиент для JSONPlaceholder
- │   ├── db/               # Сессия и инициализация БД
- │   ├── models/           # SQLAlchemy и Pydantic модели
- │   ├── services/         # Логика синхронизации и БД
- │   └── utils/            # Зависимости, планировщик
- ├── secrets/              # Docker secrets
- ├── .env                  # Переменные окружения
- ├── Dockerfile
- ├── docker-compose.yml
- ├── Makefile
- └── README.md

### API

Получение постов с фильтрацией

```bash
GET /posts
```

## Параметры

| Параметр | Тип    | Описание                                   |
|----------|--------|--------------------------------------------|
| `user_id`  | `int`   | Фильтр по ID пользователя                  |
| `title`    | `str`   | Поиск по заголовку (частичное совпадение) |
| `limit`    | `int`   | Кол-во записей (по умолчанию: 100)        |
| `username` | `str`   | Поиск по username                         |


Пример:
```bash
GET /posts?user_id=1&username=Bret
```