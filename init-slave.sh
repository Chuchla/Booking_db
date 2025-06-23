#!/bin/bash
# Czekaj, aż master będzie gotowy
until mysql -h db-master -u root -p'root_password' -e 'SELECT 1'; do
  >&2 echo "Master is unavailable - sleeping"
  sleep 10
done

>&2 echo "Master is available, configuring slave"

# Skonfiguruj replikację
mysql -u root -p'root_password' -e "
  CHANGE MASTER TO
    MASTER_HOST='db-master',
    MASTER_USER='replication_user',
    MASTER_PASSWORD='replication_password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=157,
    MASTER_CONNECT_RETRY=10;
  START SLAVE;
"