#!/bin/sh

until mariadb -h database_host -u root -p"$MYSQL_ROOT_PASSWORD" --skip-ssl -e "SELECT 1;" > /dev/null 2>&1; do
  echo "Database not ready yet... retrying in 3 seconds"
  sleep 3
done

echo "Starting Zero-Touch Archive process..."

BACKUP_FILE="/archives/backup_$(date +%F_%H-%M-%S).sql.gz"

mariadb-dump -h database_host -u root -p"$MYSQL_ROOT_PASSWORD" --all-databases --skip-ssl > $BACKUP_FILE

echo "Backup securely saved to $BACKUP_FILE"

find /archives -name "*.sql.gz" -mtime +7 -delete
echo "Old backups cleaned up."

sleep 86400