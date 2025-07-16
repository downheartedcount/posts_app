# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2025-07-16

### Added
- Подключён Poetry для управления зависимостями (`pyproject.toml`, `poetry.lock`)
- Добавлен `CORSMiddleware` с настройкой через `.env` (переменная `CORS_ORIGINS`)
- Явное логирование ошибок в `PostRepo`, `PostClient`, `routes`, с `logger.exception`
- База данных PostgreSQL больше не публикуется наружу (`ports` заменён на `expose` в `docker-compose.yml`)
- Все сервисы объединены в общую `app_net` сеть для ограничения доступа
- CORS настраивается только через `.env` (без жёстко заданных значений в `main.py`)
- Разрешённые заголовки CORS ограничены до безопасных (`Content-Type`, `Authorization`)


### Changed
- Удалены Docker secrets (`/secrets`), теперь используется только `.env` (передаётся в контейнер через `:ro`)
- Обновлён `docker-compose.yml` для безопасной передачи переменных окружения
- Рефакторинг моделей: улучшена структура `PostRequest`, добавлены ограничения через `Pydantic`

### Removed
- Удалены устаревшие `requirements.txt` и `secrets/postgres_password`
