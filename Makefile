DC = docker compose
APP_FILE = -f ./docker-compose/app.yaml
AIFLOW_FILE = -f ./docker-compose/airflow.yaml
ALL_FILES = ${AIFLOW_FILE}

ENV_FILE = --env-file ./.env

build:
	${DC} ${ALL_FILES} build
up:
	${DC} ${ALL_FILES} ${ENV_FILE} up -d --build
	make logs
up-a:
	${DC} ${ALL_FILES} ${ENV_FILE} up --build
logs:
	${DC} ${ALL_FILES} logs --follow
down:
	${DC} ${ALL_FILES} down
restart:
	make down
	make up
exec:
	docker exec -it app sh
