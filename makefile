freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

collectstatic:
	python manage.py collectstatic

migrate:
	python manage.py makemigrations
	python manage.py migrate

dev:
	python manage.py runserver