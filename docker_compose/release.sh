#!/bin/bash

IMAGE_NAME="atomowkibe/prestashop:latest"
COMPOSE_URL="https://raw.githubusercontent.com/mgdkmp13/ebiz_project/refs/heads/master/docker_compose/docker-compose.yml"
STACK_NAME="BE_193066"

echo "Pobieram docker image oraz dockercompose"
docker pull $IMAGE_NAME
wget $COMPOSE_URL -O docker-compose.yml

echo "Wdrozenie aplikacji..."
docker stack deploy -c docker-compose.yml $STACK_NAME --with-registry-auth