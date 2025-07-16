run:
	uvicorn src.main:app --reload

init-db:
	python src/db/init_db.py

install:
	poetry install --no-root

lock:
	poetry update

scan-code:
	bandit -r src/

lint:
	flake8 src/

docker-down:
	docker-compose down --volumes --remove-orphans

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f app

docker-bash:
	docker-compose exec app bash

docker-db:
	docker-compose exec db psql -U postgres -d json_app


