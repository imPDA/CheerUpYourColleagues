DC = docker compose
APP_FILE = -f ./docker-compose/app.yaml
MINIO_FILE = -f ./docker-compose/minio.yaml
ENV_FILE = --env-file ./.env

build:
	${DC} ${APP_FILE} build
up:
	${DC} ${APP_FILE} ${ENV_FILE} up -d --build
	make logs
up-a:
	${DC} ${APP_FILE} ${ENV_FILE} up --build
logs:
	${DC} ${APP_FILE} logs --follow
down:
	${DC} ${APP_FILE} down
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
