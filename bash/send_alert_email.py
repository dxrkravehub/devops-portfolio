import smtplib
from email.mime.text import MIMEText
import sys
import os

# --- КОНФИГУРАЦИЯ ПОЧТЫ ---
# Используйте "пароль приложения" для Gmail, а не основной пароль Google
# Как создать пароль приложения: https://support.google.com/accounts/answer/185833
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # Порт для STARTTLS
SENDER_EMAIL = 'ваша_почта@gmail.com'
SENDER_PASSWORD = 'ваш_пароль_приложения_gmail' # Замените на реальный пароль приложения
RECEIVER_EMAIL = 'получатель_алертов@example.com' # Или ваш_почта@gmail.com

# --- Функция отправки email ---
def send_email_alert(subject, body_content):
    msg = MIMEText(body_content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Начинаем TLS-шифрование
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email alert sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        return False

# --- Функция для анализа логов и отправки при необходимости ---
def analyze_and_alert_log(log_filepath, keywords, lines_to_check=50):
    if not os.path.exists(log_filepath):
        print(f"Log file not found: {log_filepath}", file=sys.stderr)
        return

    critical_messages = []
    try:
        with open(log_filepath, 'r', encoding='utf-8', errors='ignore') as f:
            # Читаем последние N строк (или все, если файл меньше N)
            lines = f.readlines()
            # Проверяем только последние 'lines_to_check' строк
            for line in lines[-lines_to_check:]:
                line_lower = line.lower()
                # Проверяем, содержит ли строка любое из ключевых слов
                if any(keyword.lower() in line_lower for keyword in keywords):
                    critical_messages.append(line.strip())

        if critical_messages:
            subject = f"[КРИТИЧЕСКИЙ АЛЕРТ] Обнаружены проблемы в логе: {os.path.basename(log_filepath)}"
            body = (
                f"В лог-файле {log_filepath} обнаружены следующие критические сообщения:\n\n"
                + "\n".join(critical_messages) +
                "\n\nПожалуйста, проверьте сервер немедленно."
            )
            send_email_alert(subject, body)
        else:
            print(f"No critical messages found in {log_filepath}")

    except Exception as e:
        print(f"Error processing log file {log_filepath}: {e}", file=sys.stderr)

# --- Главная часть скрипта ---
if __name__ == "__main__":
    # Пример использования:
    # Запуск: python send_alert_email.py /var/log/syslog "error" "critical" "failed"

    if len(sys.argv) < 3:
        print("Usage: python send_alert_email.py <log_filepath> <keyword1> [keyword2 ...]", file=sys.stderr)
        sys.exit(1)

    log_file = sys.argv[1]
    search_keywords = sys.argv[2:]

    analyze_and_alert_log(log_file, search_keywords)
