run:
	uvicorn src.main:app --reload

init-db:
	python src/db/init_db.py

reset-db:
	psql -h localhost -U postgres -c 'DROP DATABASE IF EXISTS json_app; CREATE DATABASE json_app;'
	make init-db

scan-safety:
	safety check --full-report --file=requirements.txt

scan-code:
	bandit -r src/

lint:
	flake8 src/

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


