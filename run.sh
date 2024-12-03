#!/bin/bash


function usage_info(){
    echo "Usage: $0 [--build] [-d]"
    echo "--build        Optional argument to build images"
    echo "-d             Optional argument to run in detached mode"
}

BUILD_OPTION=""
DETACHED_MODE=""
DOCKER_COMPOSE_DIR="./docker_compose"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --build)
            BUILD_OPTION="--build"
            ;;
        -d)
            DETACHED_MODE="-d"
            ;;
        --help)
            usage_info
            exit 0
            ;;
        *)
            echo "Invalid argument: $1"
            usage_info
            exit 1
            ;;
    esac
    shift
done


if [ -d "./prestashop" ]; then
    echo "Giving permission to prestashop folder"
    chmod -R 777 ./prestashop
    echo "Prestashop folder permission granted"
fi

if [ -d "$DOCKER_COMPOSE_DIR" ]; then
    cd "$DOCKER_COMPOSE_DIR" || exit 1  
else
    echo "Directory $DOCKER_COMPOSE_DIR does not exist!"
    exit 1
fi

echo "Starting docker-compose up $BUILD_OPTION $DETACHED_MODE"
docker-compose up $BUILD_OPTION $DETACHED_MODE
