#!/bin/bash

# Пути к данным
DATA_DIR="/var/lib/program_limiter"
DATA_FILE="$DATA_DIR/users.json"
LOG_FILE="$DATA_DIR/logs.txt"
INSTALL_TIME_FILE="$DATA_DIR/install_time.txt"
SYSTEM_ID_FILE="/etc/program_limiter/system_id"

# Проверка прав
if [ "$EUID" -ne 0 ]; then
  echo "Пожалуйста, запустите этот скрипт с правами root."
  exit 1
fi

# Установка
if [ "$1" == "install" ]; then
  echo "Установка программы..."
  mkdir -p "$DATA_DIR"
  if [ ! -f "$DATA_FILE" ]; then
    echo "{}" > "$DATA_FILE"
    echo "Создан файл $DATA_FILE"
  fi
  if [ ! -f "$LOG_FILE" ]; then
    echo "Logs initialized." > "$LOG_FILE"
    echo "Создан файл $LOG_FILE"
  fi
  if [ ! -f "$SYSTEM_ID_FILE" ]; then
    mkdir -p "/etc/program_limiter"
    uuidgen > "$SYSTEM_ID_FILE"
    echo "Создан уникальный идентификатор системы в $SYSTEM_ID_FILE"
  else
    echo "Уникальный идентификатор уже существует: $(cat $SYSTEM_ID_FILE)"
  fi
  echo "Программа успешно установлена."
  exit 0

# Удаление
elif [ "$1" == "uninstall" ]; then
  echo "Удаление программы..."
  rm -rf "$DATA_DIR"
  echo "Программа успешно удалена. Системный идентификатор сохранен."
  exit 0

else
  echo "Использование: $0 {install|uninstall}"
  exit 1
fi
