# Команды для prod
clear-volumes-prod: # Удаление Volumes
	docker compose -f infra/docker-compose-prod.yml down --volumes

start-containers-prod: # Запуск контейнеров в первый раз
	docker compose -f infra/docker-compose-prod.yml up -d;
	@sleep 3;

start-containers-prod-start: # Запуск контейнеров последующие разы
	docker compose -f infra/docker-compose-prod-start.yml up -d;
	@sleep 3;

migrate-prod: # Выполнить миграции Django
	python transcribe_app/manage.py migrate

collectstatic-prod: # Собрать статику Django
	python transcribe_app/manage.py collectstatic --noinput

createsuperuser-prod: # Создать супер пользователя
	python transcribe_app/manage.py createsuperuser --noinput

project-start-prod-in-container: # Запуск проекта в контерейнере
	make migrate-prod collectstatic-prod start-server-prod

project-init-prod-in-container: # Инициализация проекта в контерейнере
	make migrate-prod collectstatic-prod createsuperuser-prod start-server-prod

project-init-prod: # Инициализировать проект
	make clear-volumes-prod start-containers-prod

project-start-prod: # Запустить проект
	make start-containers-prod-start

start-server-prod: # Запуск сервера
	cd transcribe_app && gunicorn --bind 0.0.0.0:8000 config.wsgi

project-stop-prod: # Остановить проект
	docker compose -f infra/docker-compose-prod.yml down

# Команды для dev
clear-volumes-dev: # Удаление Volumes
	docker compose -f infra/docker-compose-dev.yml --env-file ./infra/.env down --volumes

start-containers-dev: # Запуск контейнеров
	docker compose -f infra/docker-compose-dev.yml --env-file ./infra/.env up -d;
	@sleep 3;

start-server-dev: # Запуск сервера
	python transcribe_app/manage.py runserver

migrate-dev: # Выполнить миграции Django
	python transcribe_app/manage.py migrate

createsuperuser-dev: # Создать супер пользователя
	python transcribe_app/manage.py createsuperuser --noinput

project-init-dev: # Инициализировать проект
	make clear-volumes-dev start-containers-dev migrate-dev createsuperuser-dev start-server-dev

project-start-dev: # Запустить проект
	make start-containers-dev start-server-dev

containers-stop-dev: # Остановить контейнеры
	docker compose -f docker-compose-dev.yml  --env-file ./infra/.env down
