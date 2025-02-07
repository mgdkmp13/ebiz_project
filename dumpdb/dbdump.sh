#!/bin/bash

# Konfiguracja dla backupu
DB_HOST="admin-mysql_db"        # Host bazy danych (nazwa kontenera)
DB_USER="root"              # Nazwa użytkownika bazy danych
DB_PASS="student"             # Hasło do bazy danych
DB_NAME="BE_193066"        # Nazwa bazy danych do zrzutu

# Ścieżka do zapisu pliku kopii zapasowej
BACKUP_DIR="./dump"       # Lokalizacja na hosta
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_$(date).sql"

# Tworzenie katalogu kopii zapasowej, jeśli nie istnieje
mkdir -p "$BACKUP_DIR"

# Uruchamianie zrzutu bazy danych za pomocą polecenia mysqldump w kontenerze MySQL
docker exec $DB_HOST mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_FILE"

# Sprawdzanie statusu operacji
if [ $? -eq 0 ]; then
    echo "Dump bazy danych został pomyślnie zapisany w: $BACKUP_FILE"
else
    echo "Wystąpił błąd przy tworzeniu dumpa bazy danych."
    exit 1
fi
