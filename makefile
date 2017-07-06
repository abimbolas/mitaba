freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

collectstatic:
	python manage.py collectstatic

deploy-heroku:
	git push heroku master

migrate:
	python manage.py makemigrations store
	python manage.py migrate

dev:
	python manage.py runserver