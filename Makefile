include .env
export

rebuild:
	docker-compose down
	docker-compose up --build

migrate:
	docker-compose run --rm app sh -c "python manage.py makemigrations"

create_user:
	docker-compose run --rm app sh -c "python manage.py createsuperuser"

create_bots:
	docker-compose run --rm app sh -c "python manage.py create_bots"
