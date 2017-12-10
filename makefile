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
	ssh mitabadev@mitaba.ru "cd /projects/mitaba.ru && make down && make up"

deploy-check-ps:
	ssh mitabadev@mitaba.ru "cd /projects/mitaba.ru && docker ps"

deploy-changes:
	docker-compose -f docker-compose.production.yml build --force-rm --pull
	docker push antivitla/mitaba
	git push
	ssh mitabadev@mitaba.ru "cd /projects/mitaba.ru && make down && make up"

copy-production-settings:
	scp host/django/settings.production.py mitabadev@mitaba.ru:/projects/mitaba.ru/host/django/settings.production.py


# Local development
dev-up:
	docker-compose -f docker-compose.production.yml -f docker-compose.development.yml up

dev-down:
	docker-compose -f docker-compose.production.yml -f docker-compose.development.yml down

dev-build:
	docker-compose -f docker-compose.production.yml build --force-rm --pull
