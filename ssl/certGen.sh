#!/bin/bash

sudo apt update
sudo apt install -y openssl

mkdir -p /etc/apache2/private
mkdir -p /etc/apache2/certs

openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/apache2/private/selfKey.key -out /etc/apache2/certs/selfCert.crt -subj "/C=US/ST=State/L=City/O=Company/OU=Department/CN=localhost"

chown www-data:www-data /etc/apache2/private/selfKey.key /etc/apache2/certs/selfCert.crt