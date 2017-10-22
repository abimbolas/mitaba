# Migrate database
migrate:
	python manage.py makemigrations
	python manage.py migrate

# Dump database
dumpdata:
	python manage.py dumpdata --indent 2 --output /dumpdata/dumpdata.json

# Load from database dump
loaddata:
	python manage.py loaddata /dumpdata/dumpdata.json

# Crate superuser
superuser:
	python manage.py createsuperuser
