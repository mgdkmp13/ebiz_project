#!/bin/bash

# Konfiguracja dla backupu
DB_HOST="ebiz-mysql"        # Host bazy danych (nazwa kontenera)
DB_USER="root"              # Nazwa użytkownika bazy danych
DB_PASS="admin"             # Hasło do bazy danych
DB_NAME="prestashop"        # Nazwa bazy danych do zrzutu

# Ścieżka do zapisu pliku kopii zapasowej
BACKUP_DIR="./dump"       # Lokalizacja na hosta
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_$(date).sql"

# Tworzenie katalogu kopii zapasowej, jeśli nie istnieje
mkdir -p "$BACKUP_DIR"

# Uruchamianie zrzutu bazy danych za pomocą polecenia mysqldump w kontenerze MySQL
docker exec ebiz-mysql mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_FILE"

# Sprawdzanie statusu operacji
if [ $? -eq 0 ]; then
    echo "Dump bazy danych został pomyślnie zapisany w: $BACKUP_FILE"
else
    echo "Wystąpił błąd przy tworzeniu dumpa bazy danych."
fi
