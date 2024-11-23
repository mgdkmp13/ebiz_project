Aby wykonać dump bazy danych:
./dbdump.sh

Aby zasilic baze danych przy następnym uruchomieniu danymi z dbdump (wywołac z głownego katalogu tam gdzie jest docker-compose)
cp ./dumpdb/dump/nazwa.sql ./db_init/