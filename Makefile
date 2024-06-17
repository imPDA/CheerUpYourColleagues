DC = docker compose
APP_FILE = -f ./docker-compose/app.yaml
AIFLOW_FILE = -f ./docker-compose/airflow.yaml
MINIO_FILE = -f ./docker-compose/minio.yaml
ENV_FILE = --env-file ./.env

build:
	${DC} ${AIFLOW_FILE} build
up:
	${DC} ${AIFLOW_FILE} ${ENV_FILE} up -d --build
	make logs
up-a:
	${DC} ${AIFLOW_FILE} ${ENV_FILE} up --build
logs:
	${DC} ${AIFLOW_FILE} logs --follow
down:
	${DC} ${AIFLOW_FILE} down
restart:
	make down
	make up
exec:
	docker exec -it app sh

minio-up:
	${DC} ${MINIO_FILE} up -d

minio-logs:
	${DC} ${MINIO_FILE} logs --follow

minio-down:
	${DC} ${MINIO_FILE} down

export-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
