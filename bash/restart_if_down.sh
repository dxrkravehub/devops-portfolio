#!/bin/bash
# Скрипт проверки и условного перезапуска службы Plex
SERVICE_NAME="plexmediaserver" # Пример службы
LOG_FILE="/var/log/service_restart.log"

if ! systemctl is-active --quiet $SERVICE_NAME; then
    echo "$(date): Service $SERVICE_NAME is not running. Attempting to restart..." >> $LOG_FILE
    systemctl restart $SERVICE_NAME
    sleep 5 # Даем время на запуск
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo "$(date): Service $SERVICE_NAME restarted successfully." >> $LOG_FILE
    else
        echo "$(date): Failed to restart $SERVICE_NAME. Manual intervention required." >> $LOG_FILE
    fi
fi
