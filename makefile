up-dev:
	docker-compose -f docker-compose.production.yml -f docker-compose.development.yml up

down-dev:
	docker-compose -f docker-compose.production.yml -f docker-compose.development.yml down

up:
	git pull
	docker pull antivitla/mitaba
	docker-compose -f docker-compose.production.yml up -d

down:
	docker-compose -f docker-compose.production.yml down

build:
	docker-compose -f docker-compose.production.yml build --force-rm --pull
	docker login
	docker push antivitla/mitaba



