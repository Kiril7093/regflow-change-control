.PHONY: up down logs migrate run shell-db createsuperuser

up:
	docker compose up -d db

down:
	docker compose down

logs:
	docker compose logs -f db

migrate:
	cd backend && python manage.py migrate

createsuperuser:
	cd backend && python manage.py createsuperuser

run:
	cd backend && python manage.py runserver 0.0.0.0:8000

shell-db:
	docker compose exec db psql -U $${POSTGRES_USER:-regflow} -d $${POSTGRES_DB:-regflow}
