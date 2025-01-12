#!/bin/bash

MYSQL_HOST="admin-mysql_default"
MYSQL_PORT="3306"
MYSQL_USER="root"
MYSQL_PASSWORD="student"
MYSQL_DATABASE="BE_193066"

SQL_DUMP_FILE="/db_init/presta_init.sql"

echo "Tworze db"
mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};"

echo "Seeduje db"
mysql -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$SQL_DUMP_FILE"

echo "Usuwam katalogi"
if [ -d "install" ]; then
    rm -rf install
fi

echo "Inizjalizacja zakonczona"

echo "Server Start"
exec apache2-foreground