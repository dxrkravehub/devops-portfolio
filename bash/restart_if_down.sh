#!/bin/bash
# Скрипт проверки и условного перезапуска службы Plex
SERVICE_NAME="plexmediaserver" # Пример службы
# Лог-файл, который нужно проверить
# Или /var/log/apache2/error.log, /var/log/nginx/error.log, и т.д.
# Ключевые слова для поиска в логах (через пробел)
LOG_FILE="/var/log/service_restart.log"
PYTHON_SCRIPT="/path/to/your/send_alert_email.py"
KEYWORDS=("error" "critical" "failed" "denied" "disk full")
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
# Вызываем Python-скрипт с нужными параметрами
python3 "$PYTHON_SCRIPT" "$LOG_FILE" "${KEYWORDS[@]}"

# Вывод Python-скрипта будет в STDOUT/STDERR Bash-скрипта.
# Вы можете перенаправить его в лог Bash-скрипта, если нужно.

