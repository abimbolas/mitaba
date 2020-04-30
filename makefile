# Admin
up:
	git pull
	docker pull antivitla/mitaba
	docker-compose -f docker-compose.production.yml up -d
	docker exec mitaba_app bash -c "make migrate"

down:
	docker-compose -f docker-compose.production.yml down

dumpdata:
	docker exec mitaba_app bash -c "make dumpdata"

# Deploy
deploy-restart:
	ssh antivitla@mitaba.ru "cd /projects/mitaba.ru && make down && make up"

deploy-check-ps:
	ssh antivitla@mitaba.ru "cd /projects/mitaba.ru && docker ps"

deploy-changes:
	docker-compose -f docker-compose.production.yml build --force-rm --pull
	docker push antivitla/mitaba
	git push
	ssh antivitla@mitaba.ru "cd /projects/mitaba.ru && make down && make up"

deploy-docker-image:
	docker-compose -f docker-compose.production.yml build --force-rm --pull
	docker push antivitla/mitaba

copy-production-settings:
	scp host/django/settings.production.py antivitla@mitaba.ru:/projects/mitaba.ru/host/django/settings.production.py


# Local development
dev-up:
	docker-compose -f docker-compose.production.yml -f docker-compose.development.yml up

dev-down:
	docker-compose -f docker-compose.production.yml -f docker-compose.development.yml down

dev-build:
	docker-compose -f docker-compose.production.yml build --force-rm --pull

dev-cert:
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout host/cert/local.key -out host/cert/local.crt -config host/cert/local.conf
	openssl rsa -in host/cert/local.key -out host/cert/local.key
