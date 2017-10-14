docker-compose -f docker-compose.production.yml build --force-rm --pull
docker login
docker push antivitla/mitaba
