#!/bin/bash

# Variables
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/tmp/mongodb_backup_$TIMESTAMP"
S3_BUCKET="playground-2-s3-mongo-backups"
S3_PATH="mongodb_backups"

# Create backup directory (locally)
mkdir -p $BACKUP_DIR

# Run MongoDB dump (locally)
mongodump --out=$BACKUP_DIR

# Compress the backup (locally)
tar -czf "$BACKUP_DIR.tar.gz" $BACKUP_DIR

# Upload to S3
aws s3 cp "$BACKUP_DIR.tar.gz" "s3://$S3_BUCKET/$S3_PATH/mongodb_backup_$TIMESTAMP.tar.gz"

# Clean up local files
rm -rf $BACKUP_DIR
rm -f "$BACKUP_DIR.tar.gz"