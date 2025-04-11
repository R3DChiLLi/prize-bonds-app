#!/bin/bash

# Define variables
DB_USER="root"                  # MySQL username
DB_PASS="admin123"         # MySQL password
DB_NAME="SerialRecords"         # Database name
BACKUP_DIR="/home/ec2-user/app/backups_sql/"   # Directory where backups will be stored
TIMESTAMP=$(date +"%Y%m%d_%H%M%S") # Timestamp for unique filenames

# Create a backup file
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/SerialRecords_backup_$TIMESTAMP.sql

# Optional: Remove backups older than 7 days
find $BACKUP_DIR -type f -name "*.sql" -mtime +7 -exec rm {} \;

