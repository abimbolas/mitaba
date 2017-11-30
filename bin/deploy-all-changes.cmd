docker-compose -f docker-compose.production.yml build --force-rm --pull
docker push antivitla/mitaba
git push
bin\deploy-restart.cmd
bin\copy-production-settings.cmd
