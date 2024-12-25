import os
import sys
import time
import json
from datetime import datetime, timedelta

# Пути для хранения данных
DATA_FILE = "/var/lib/program_limiter/users.json"
LOG_FILE = "/var/lib/program_limiter/logs.txt"
INSTALL_TIME_FILE = "/var/lib/program_limiter/install_time.txt"
SYSTEM_ID_FILE = "/etc/program_limiter/system_id"
SYSTEM_USAGE_FILE = "/etc/program_limiter/system_usage.json"

# Глобальные лимиты
GLOBAL_LIMIT = 5  # Лимит запусков
LIFETIME_LIMIT_SECONDS = 60  # Лимит времени существования программы на системе

def load_data(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def get_system_id():
    if os.path.exists(SYSTEM_ID_FILE):
        with open(SYSTEM_ID_FILE, 'r') as f:
            return f.read().strip()
    else:
        return None

def main():
    # Проверка системного идентификатора
    system_id = get_system_id()
    if not system_id:
        print("Ошибка: системный идентификатор не найден. Переустановите программу.")
        sys.exit(1)
    print(f"Системный идентификатор: {system_id}")

    # Проверка времени жизни программы
    if not os.path.exists(INSTALL_TIME_FILE):
        with open(INSTALL_TIME_FILE, 'w') as f:
            f.write(datetime.now().isoformat())
    else:
        with open(INSTALL_TIME_FILE, 'r') as f:
            install_time = datetime.fromisoformat(f.read().strip())
        if datetime.now() - install_time > timedelta(seconds=LIFETIME_LIMIT_SECONDS):
            print("Срок действия программы истек. Хотите купить полную версию? (да/нет)")
            choice = input().strip().lower()
            if choice == 'да':
                print("Спасибо за интерес к полной версии!")
                sys.exit()
            else:
                uninstall()

    # Загрузка данных пользователей и системы
    data = load_data(DATA_FILE)
    usage_data = load_data(SYSTEM_USAGE_FILE)

    # Проверка оставшихся запусков
    remaining_runs = usage_data.get(system_id, GLOBAL_LIMIT)
    if remaining_runs <= 0:
        print("Вы достигли лимита использования программы. Хотите купить полную версию? (да/нет)")
        choice = input().strip().lower()
        if choice == 'да':
            print("Спасибо за интерес к полной версии!")
            sys.exit()
        else:
            uninstall()

    # Запрос данных пользователя
    print("Введите ваше ФИО:")
    full_name = input().strip()

    if full_name in data:
        print("Такое ФИО уже зарегистрировано. Добро пожаловать обратно!")
    else:
        data[full_name] = True
        print("Ваше ФИО успешно зарегистрировано.")

    # Уменьшение лимита запусков
    usage_data[system_id] = remaining_runs - 1
    print(f"Запусков осталось: {remaining_runs - 1}")

    save_data(DATA_FILE, data)
    save_data(SYSTEM_USAGE_FILE, usage_data)
    log(f"Пользователь {full_name} запустил программу. Осталось запусков: {remaining_runs - 1}")

def uninstall():
    print("Программа будет удалена.")
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    if os.path.exists(INSTALL_TIME_FILE):
        os.remove(INSTALL_TIME_FILE)
    print("Программа успешно удалена. Учет использования сохранен.")
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")
