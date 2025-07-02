#!/bin/bash
# Скрипт для очистки старых лог-файлов
LOG_DIR="/var/log/"
MEDIA_SERVER_LOG_DIR="/opt/plex/Library/Application Support/Plex Media Server/Logs/" # Пример пути
FIND_AGE="+30" # Файлы старше 30 дней

echo "$(date): log cleanup..." >> /var/log/cleanup_logs.log
find "$LOG_DIR" -type f -name "*.log" -mtime $FIND_AGE -delete -print >> /var/log/cleanup_logs.log
find "$MEDIA_SERVER_LOG_DIR" -type f -name "*.log" -mtime $FIND_AGE -delete -print >> /var/log/cleanup_logs.log
echo "$(date): Log cleanup finished." >> /var/log/cleanup_logs.log
