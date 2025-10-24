.PHONY: build start stop restart makemigrations migrate logs check shell

build:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

check:
	docker-compose exec web python manage.py check

shell:
	docker-compose exec web python manage.py shell

