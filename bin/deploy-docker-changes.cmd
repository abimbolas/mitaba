docker-compose -f docker-compose.production.yml build --force-rm --pull
docker push antivitla/mitaba
bin\deploy-restart.cmd
